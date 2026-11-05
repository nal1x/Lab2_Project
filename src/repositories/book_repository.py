from database.database import get_connection
from models.book import Book

def _map(row) -> Book:
    return Book(*row)

def create(title: str, author_id: int, genre: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Books(title, author_id, genre) VALUES (?, ?, ?)", (title, author_id, genre))
    conn.commit()
    conn.close()

def get_all() -> list[Book]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT book_id, title, author_id, genre FROM Books")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(book_id: int) -> Book | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT book_id, title, author_id, genre FROM Books WHERE book_id = ?", (book_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_author(author_id: int) -> list[Book]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT book_id, title, author_id, genre FROM Books WHERE author_id = ?", (author_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update(book_id: int, title: str, author_id: int, genre: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Books SET title = ?, author_id = ?, genre = ? WHERE book_id = ?", (title, author_id, genre, book_id))
    conn.commit()
    conn.close()

def delete(book_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Books WHERE book_id = ?", (book_id,))
    conn.commit()
    conn.close()

def search_by_title(title: str) -> list[Book]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT book_id, title, author_id, genre FROM Books WHERE title LIKE ?", ('%' + title + '%',))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]