
import csv
import json
import os
import xml.etree.ElementTree as ET
import yaml

import database.database as db


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
                else:
                    element.text = "" if item is None else str(item)
        else:
            child.text = "" if value is None else str(value)


def get_table_data(table_name):
    conn = db.get_connection()

    try:
        cursor = conn.cursor()

        # Получаем столбцы главной таблицы
        cursor.execute(f'PRAGMA table_info("{table_name}")')
        columns = [row[1] for row in cursor.fetchall()]

        if not columns:
            raise ValueError("Таблица не найдена!")

        # Получаем внешние ключи
        cursor.execute(f'PRAGMA foreign_key_list("{table_name}")')
        foreign_keys = cursor.fetchall()

        select_parts = [
            f'main."{col}" AS "main__{col}"'
            for col in columns
        ]

        join_parts = []

        for index, fk in enumerate(foreign_keys):
            ref_table = fk[2]
            from_col = fk[3]
            to_col = fk[4]

            group_name = (
                from_col[:-3]
                if from_col.endswith("_id")
                else ref_table
            )

            alias = f"rel_{index}"

            cursor.execute(f'PRAGMA table_info("{ref_table}")')
            ref_columns = [
                row[1] for row in cursor.fetchall()
            ]

            for col in ref_columns:
                select_parts.append(
                    f'{alias}."{col}" AS "{group_name}__{col}"'
                )

            join_parts.append(
                f'LEFT JOIN "{ref_table}" {alias} '
                f'ON main."{from_col}" = {alias}."{to_col}"'
            )

        # Формируем SQL-запрос
        sql = (
            f'SELECT {", ".join(select_parts)} '
            f'FROM "{table_name}" main '
            f'{" ".join(join_parts)}'
        )

        cursor.execute(sql)

        names = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    finally:
        conn.close()

    nested_data = []
    flat_data = []

    for row in rows:
        nested_item = {}
        flat_item = {}

        for name, value in zip(names, row):
            group, field = name.split("__", 1)

            if group == "main":
                flat_item[field] = value

                if field not in [
                    fk[3] for fk in foreign_keys
                ]:
                    nested_item[field] = value

            else:
                flat_item[f"{group}_{field}"] = value

                if group not in nested_item:
                    nested_item[group] = {}

                nested_item[group][field] = value

        for key, value in list(nested_item.items()):
            if isinstance(value, dict):
                if all(v is None for v in value.values()):
                    nested_item[key] = None

        nested_data.append(nested_item)
        flat_data.append(flat_item)

    return nested_data, flat_data


def auto_export(table_name):
    # Создаём папку out
    project_dir = os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)
    ))

    out_dir = os.path.join(project_dir, "out")
    os.makedirs(out_dir, exist_ok=True)

    # Получаем данные из базы
    nested_data, flat_data = get_table_data(table_name)

    # JSON
    with open(os.path.join(out_dir, "data.json"),
              "w", encoding="utf-8") as file:
        json.dump(
            nested_data,
            file,
            ensure_ascii=False,
            indent=4
        )

    # YAML
    with open(os.path.join(out_dir, "data.yaml"),
              "w", encoding="utf-8") as file:
        yaml.safe_dump(
            nested_data,
            file,
            allow_unicode=True,
            sort_keys=False
        )

    # XML
    root = ET.Element(f"{table_name}_list")

    for item in nested_data:
        record = ET.SubElement(root, table_name)
        dict_to_xml(record, item)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ")

    tree.write(
        os.path.join(out_dir, "data.xml"),
        encoding="utf-8",
        xml_declaration=True
    )

    # CSV
    if flat_data:
        headers = list(flat_data[0].keys())

        with open(os.path.join(out_dir, "data.csv"),
                  "w", encoding="utf-8-sig",
                  newline="") as file:

            writer = csv.DictWriter(
                file,
                fieldnames=headers
            )

            writer.writeheader()
            writer.writerows(flat_data)

    print("Данные успешно экспортированы!")
    print("Файлы находятся в папке out.")
