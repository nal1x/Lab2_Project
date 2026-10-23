import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'library.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

conn.commit()
conn.close()



