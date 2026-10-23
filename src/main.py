import os
import sqlite3

dir_path = os.path.dirname(__file__)
db_path = os.path.join(dir_path, 'library.db')
sql_path = os.path.join(dir_path, 'schema.sql')

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.executescript(open(sql_path, encoding='utf-8').read())

    cursor.execute("SELECT * FROM Books")
    for book in cursor.fetchall():
        print(book)
