from database.database import get_connection
from models.book import Book

def _map(row) -> Book:
    return Book(*row)

def create(title: str, author_id: int, genre: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Books(title, author_id, genre)
        VALUES (?, ?, ?)
    """, (title, author_id, genre))
    conn.commit()
    conn.close()

def get_all() -> list[Book]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT book_id, title, author_id, genre FROM Books")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]