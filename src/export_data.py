
import csv
import json
import os
import re
import xml.etree.ElementTree as ET

import yaml

import database.database as db


def quote_identifier(name):
    """Безопасное оформление имён таблиц и столбцов."""
    return '"' + str(name).replace('"', '""') + '"'


def find_table_with_relations(cursor):
    """Поиск таблицы с внешними ключами."""
    cursor.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' "
        "ORDER BY name"
    )

    tables = [row[0] for row in cursor.fetchall()]

    for table_name in tables:
        cursor.execute(
            f"PRAGMA foreign_key_list({quote_identifier(table_name)})"
        )

        if cursor.fetchall():
            return table_name

    raise ValueError("Не найдена таблица со связями!")


def dict_to_xml(parent, data):
    """Преобразование словаря в XML."""
    for key, value in data.items():
        child = ET.SubElement(parent, str(key))

        if isinstance(value, dict):
            dict_to_xml(child, value)

        elif isinstance(value, list):
            for item in value:
                element = ET.SubElement(child, "item")

                if isinstance(item, dict):
                    dict_to_xml(element, item)

                elif item is not None:
                    element.text = str(item)

        elif value is not None:
            child.text = str(value)


def get_table_data(table_name=None):
    """Получение данных основной и связанных таблиц."""
    conn = db.get_connection()

    try:
        cursor = conn.cursor()

        if table_name is None:
            table_name = find_table_with_relations(cursor)

        cursor.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name = ?",
            (table_name,)
        )

        if cursor.fetchone() is None:
            raise ValueError(
                f"Таблица '{table_name}' не найдена!"
            )

        table_sql = quote_identifier(table_name)

        cursor.execute(f"PRAGMA table_info({table_sql})")
        columns = [row[1] for row in cursor.fetchall()]

        if not columns:
            raise ValueError("В таблице нет столбцов!")

        cursor.execute(
            f"PRAGMA foreign_key_list({table_sql})"
        )

        foreign_keys = cursor.fetchall()

        select_parts = []
        join_parts = []
        related_info = []

        # Получаем столбцы основной таблицы.
        for column in columns:
            select_parts.append(
                f'main.{quote_identifier(column)} '
                f'AS {quote_identifier("main__" + column)}'
            )

        # Получаем информацию о связанных таблицах.
        used_group_names = set()

        for index, fk in enumerate(foreign_keys):
            ref_table = fk[2]
            from_column = fk[3]
            to_column = fk[4]

            alias = f"related_{index}"

            if from_column.endswith("_id"):
                group_name = from_column[:-3]
            else:
                group_name = ref_table.lower()

            if not group_name or group_name in used_group_names:
                group_name = f"{ref_table.lower()}_{index + 1}"

            used_group_names.add(group_name)

            ref_table_sql = quote_identifier(ref_table)

            cursor.execute(
                f"PRAGMA table_info({ref_table_sql})"
            )

            ref_columns = [
                row[1] for row in cursor.fetchall()
            ]

            related_info.append({
                "group": group_name,
                "alias": alias,
                "columns": ref_columns,
                "key": to_column
            })

            for column in ref_columns:
                alias_name = f"{alias}__{column}"

                select_parts.append(
                    f'{alias}.{quote_identifier(column)} '
                    f'AS {quote_identifier(alias_name)}'
                )

            # Связываем таблицы через LEFT JOIN.
            join_parts.append(
                f"LEFT JOIN {ref_table_sql} {alias} "
                f"ON main.{quote_identifier(from_column)} "
                f"= {alias}.{quote_identifier(to_column)}"
            )

        # Формируем SQL-запрос.
        sql = (
            f"SELECT {', '.join(select_parts)} "
            f"FROM {table_sql} AS main "
            f"{' '.join(join_parts)}"
        )

        cursor.execute(sql)

        rows = cursor.fetchall()

        result_columns = [
            column[0] for column in cursor.description
        ]

    finally:
        conn.close()

    nested_data = []
    flat_data = []

    foreign_key_columns = {
        fk[3] for fk in foreign_keys
    }

    # Формируем вложенные и плоские данные.
    for row in rows:
        nested_item = {}
        flat_item = {}

        for name, value in zip(result_columns, row):
            if name.startswith("main__"):
                column = name[len("main__"):]

                flat_item[column] = value

                if column not in foreign_key_columns:
                    nested_item[column] = value

        # Добавляем информацию связанных таблиц.
        for info in related_info:
            related_item = {}

            for column in info["columns"]:
                result_name = f'{info["alias"]}__{column}'

                value = row[result_columns.index(result_name)]

                related_item[column] = value

                if column != info["key"]:
                    flat_item[
                        f'{info["group"]}_{column}'
                    ] = value

            if all(
                value is None
                for value in related_item.values()
            ):
                nested_item[info["group"]] = None
            else:
                nested_item[info["group"]] = related_item

        nested_data.append(nested_item)
        flat_data.append(flat_item)

    # Формируем заголовки CSV.
    flat_headers = list(columns)

    for info in related_info:
        for column in info["columns"]:
            if column != info["key"]:
                header = f'{info["group"]}_{column}'

                if header not in flat_headers:
                    flat_headers.append(header)

    return table_name, nested_data, flat_data, flat_headers


def auto_export(table_name="Books"):
    """Экспорт данных в JSON, CSV, XML и YAML."""

    # Определяем папку проекта.
    project_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    # Создаём папку out.
    out_dir = os.path.join(project_dir, "out")
    os.makedirs(out_dir, exist_ok=True)

    # Получаем данные из базы данных.
    table_name, nested_data, flat_data, flat_headers = (
        get_table_data(table_name)
    )

    # 1. JSON
    json_path = os.path.join(out_dir, "data.json")

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(
            nested_data,
            file,
            ensure_ascii=False,
            indent=4
        )

    # 2. CSV
    csv_path = os.path.join(out_dir, "data.csv")

    with open(
        csv_path,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=flat_headers
        )

        writer.writeheader()
        writer.writerows(flat_data)

    # 3. XML
    root_name = re.sub(
        r"[^A-Za-z0-9_.-]",
        "_",
        str(table_name)
    )

    if not root_name or not re.match(r"[A-Za-z_]", root_name[0]):
        root_name = "table_" + root_name

    root = ET.Element(f"{root_name}_list")

    for item in nested_data:
        record = ET.SubElement(root, root_name)
        dict_to_xml(record, item)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ")

    xml_path = os.path.join(out_dir, "data.xml")

    tree.write(
        xml_path,
        encoding="utf-8",
        xml_declaration=True
    )

    # 4. YAML
    yaml_path = os.path.join(out_dir, "data.yaml")

    with open(yaml_path, "w", encoding="utf-8") as file:
        yaml.safe_dump(
            nested_data,
            file,
            allow_unicode=True,
            sort_keys=False
        )

    print("Данные успешно экспортированы!")
    print("Созданы файлы:")
    print("data.json")
    print("data.csv")
    print("data.xml")
    print("data.yaml")
    print(f"Папка: {out_dir}")


if __name__ == "__main__":
    auto_export("Books")
