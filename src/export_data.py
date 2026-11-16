
import csv
import json
import os
import xml.etree.ElementTree as ET

import yaml

import database.database as db


def quote_identifier(name):
    return '"' + name.replace('"', '""') + '"'


def dict_to_xml(parent, data):
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


def get_table_data(table_name):
    conn = db.get_connection()

    try:
        cursor = conn.cursor()

        # Проверяем существование таблицы
        cursor.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name = ?",
            (table_name,)
        )

        if cursor.fetchone() is None:
            raise ValueError(
                f"Таблица {table_name} не найдена!"
            )

        table = quote_identifier(table_name)

        # Получаем столбцы главной таблицы
        cursor.execute(f"PRAGMA table_info({table})")

        columns = [
            row[1] for row in cursor.fetchall()
        ]

        # Получаем внешние ключи
        cursor.execute(
            f"PRAGMA foreign_key_list({table})"
        )

        foreign_keys = cursor.fetchall()

        select_parts = []
        join_parts = []
        related_info = []

        # Добавляем столбцы главной таблицы
        for column in columns:
            select_parts.append(
                f'main.{quote_identifier(column)} '
                f'AS "main__{column}"'
            )

        # Получаем связанные данные
        for index, fk in enumerate(foreign_keys):
            ref_table = fk[2]
            from_column = fk[3]
            to_column = fk[4]

            alias = f"rel_{index}"

            group_name = (
                from_column[:-3]
                if from_column.endswith("_id")
                else ref_table.lower()
            )

            if group_name in columns:
                group_name = ref_table.lower()

            ref_table_sql = quote_identifier(ref_table)

            # Получаем столбцы связанной таблицы
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
                select_parts.append(
                    f'{alias}.{quote_identifier(column)} '
                    f'AS "{alias}__{column}"'
                )

            # Создаём связь между таблицами
            join_parts.append(
                f'LEFT JOIN {ref_table_sql} {alias} '
                f'ON main.{quote_identifier(from_column)} '
                f'= {alias}.{quote_identifier(to_column)}'
            )

        # Формируем SQL-запрос
        sql = (
            f'SELECT {", ".join(select_parts)} '
            f'FROM {table} main '
            f'{" ".join(join_parts)}'
        )

        cursor.execute(sql)

        rows = cursor.fetchall()
        names = [
            column[0] for column in cursor.description
        ]

    finally:
        conn.close()

    nested_data = []
    flat_data = []

    # Формируем данные для JSON, XML и YAML
    # и отдельные строки для CSV
    for row in rows:
        nested_item = {}
        flat_item = {}

        for name, value in zip(names, row):
            if name.startswith("main__"):
                column = name[6:]

                flat_item[column] = value

                # Внешний ключ остаётся в CSV,
                # но связанная информация будет вложенной
                if column not in [
                    fk[3] for fk in foreign_keys
                ]:
                    nested_item[column] = value

        for info in related_info:
            alias = info["alias"]
            group_name = info["group"]
            key_column = info["key"]

            related_item = {}

            for column in info["columns"]:
                name = f"{alias}__{column}"
                value = row[names.index(name)]

                related_item[column] = value

                # Не дублируем внешний ключ в CSV
                if column != key_column:
                    flat_item[
                        f"{group_name}_{column}"
                    ] = value

            # Если связанной записи нет
            if all(
                value is None
                for value in related_item.values()
            ):
                nested_item[group_name] = None
            else:
                nested_item[group_name] = related_item

        nested_data.append(nested_item)
        flat_data.append(flat_item)

    # Заголовки CSV формируются даже при пустой таблице
    flat_headers = list(columns)

    for info in related_info:
        for column in info["columns"]:
            if column != info["key"]:
                flat_headers.append(
                    f'{info["group"]}_{column}'
                )

    return nested_data, flat_data, flat_headers


def auto_export(table_name):
    # Определяем папку проекта
    project_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    # Создаём папку out, если её нет
    out_dir = os.path.join(project_dir, "out")
    os.makedirs(out_dir, exist_ok=True)

    # Получаем данные из базы
    nested_data, flat_data, flat_headers = (
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

    # 2. YAML
    yaml_path = os.path.join(out_dir, "data.yaml")

    with open(yaml_path, "w", encoding="utf-8") as file:
        yaml.safe_dump(
            nested_data,
            file,
            allow_unicode=True,
            sort_keys=False
        )

    # 3. XML
    root = ET.Element(f"{table_name}_list")

    for item in nested_data:
        record = ET.SubElement(root, table_name)
        dict_to_xml(record, item)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ")

    xml_path = os.path.join(out_dir, "data.xml")

    tree.write(
        xml_path,
        encoding="utf-8",
        xml_declaration=True
    )

    # 4. CSV
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

    print("Данные успешно экспортированы!")
    print("Созданы файлы:")
    print("data.json")
    print("data.csv")
    print("data.xml")
    print("data.yaml")
    print(f"Папка: {out_dir}")


if __name__ == "__main__":
    auto_export("Books")
