import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'library.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT * FROM Books")
books = cursor.fetchall()

for book in books:
    print(book)

conn.commit()
conn.close()



