from database.database import get_connection
from models.author import Author

def _map(row) -> Author:
    return Author(*row)

def create(name: str, surname: str, patronymic: str | None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Authors(name, surname, patronymic) VALUES (?, ?, ?)", (name, surname, patronymic))
    conn.commit()
    conn.close()

def get_all() -> list[Author]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT author_id, name, surname, patronymic FROM Authors")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(author_id: int) -> Author | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT author_id, name, surname, patronymic FROM Authors WHERE author_id = ?", (author_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_exact(name: str, surname: str, patronymic: str | None) -> Author | None:
    conn = get_connection()
    cur = conn.cursor()
    if patronymic:
        cur.execute("SELECT author_id, name, surname, patronymic FROM Authors WHERE name = ? AND surname = ? AND patronymic = ?", (name, surname, patronymic))
    else:
        cur.execute("SELECT author_id, name, surname, patronymic FROM Authors WHERE name = ? AND surname = ? AND patronymic IS NULL", (name, surname))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def update(author_id: int, name: str, surname: str, patronymic: str | None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Authors SET name = ?, surname = ?, patronymic = ? WHERE author_id = ?", (name, surname, patronymic, author_id))
    conn.commit()
    conn.close()

def delete(author_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Authors WHERE author_id = ?", (author_id,))
    conn.commit()
    conn.close()