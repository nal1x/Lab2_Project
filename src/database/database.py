import sqlite3
import os

def get_connection():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'library.db')
    return sqlite3.connect(db_path)

def init_db():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'library.db')
    sql_path = os.path.join(base_dir, 'schema.sql')
    if not os.path.exists(db_path):
        with sqlite3.connect(db_path) as conn:
            with open(sql_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()