"""import os
import sqlite3

dir_path = os.path.dirname(__file__)
db_path = os.path.join(dir_path, 'library.db')
sql_path = os.path.join(dir_path, 'schema.sql')

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.executescript(open(sql_path, encoding='utf-8').read())

    cursor.execute("SELECT * FROM Books")
    for book in cursor.fetchall():
        print(book)"""
from ui.auth import login
from ui.menu import admin_menu, reader_menu

if __name__ == "__main__":
    while True:
        user = login()
        if user:
            if user.role_id == 1:
                admin_menu(user)
            elif user.role_id == 2:
                reader_menu(user)
        retry = input("\nХотите войти снова? (1 - да, 0 - выход из программы): ")
        if retry == "0":
            print("Завершение работы программы...")
            break
