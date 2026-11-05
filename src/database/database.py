import sqlite3
import os


def get_connection():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'library.db')
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sql_path = os.path.join(base_dir, 'schema.sql')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name IN ('Roles', 'Authors', 'Users', 'Books', 'Bookings')")

    if cur.fetchone()[0] != 5:
        with open(sql_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()

        from services import user_service
        try:
            if not user_service.get_all():
                user_service.create_user('Алексей', 'Смирнов', '', 1, 'admin', 'admin123')
                user_service.create_user('Иван', 'Иванов', 'Иванович', 2, 'ivan', '1234')
                user_service.create_user('Анна', 'Петрова', 'Сергеевна', 2, 'anna', '1234')
        except Exception:
            pass

    conn.close()