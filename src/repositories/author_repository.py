from database.database import get_connection
from models.author import Author

def _map(row) -> Author:
    return Author(*row)

def create(name: str, surname: str, patronymic: str | None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO authors(name, surname, patronymic)
        VALUES (?, ?, ?)
    """, (name, surname, patronymic))
    conn.commit()
    conn.close()

def get_all() -> list[Author]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT author_id, name, surname, patronymic
        FROM authors
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]