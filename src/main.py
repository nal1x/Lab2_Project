import sqlite3
from pathlib import Path

# Определяем папку с файлами проекта
folder = Path(__file__).resolve().parent

# Подключаемся к базе данных
conn = sqlite3.connect(folder / "library.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

# Выполняем команды из файла schema.sql
with open(folder / "schema.sql", "r", encoding="utf-8") as file:
    cursor.executescript(file.read())

conn.commit()

# Выводим список авторов
cursor.execute("SELECT * FROM Authors")
authors = cursor.fetchall()

print("Авторы в базе данных:")
for author in authors:
    print(author)

# Выводим список книг
cursor.execute("SELECT * FROM Books")
books = cursor.fetchall()

print("\nКниги в базе данных:")
for book in books:
    print(book)

# Закрываем подключение
conn.close()


