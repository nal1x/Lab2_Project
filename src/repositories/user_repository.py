from database.database import get_connection
from models.user import User

def _map(row) -> User:
    return User(*row)

def create(name: str, surname: str, patronymic: str | None, role_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Users(name, surname, patronymic, role_id)
        VALUES (?, ?, ?, ?)
    """, (name, surname, patronymic, role_id))
    conn.commit()
    conn.close()

def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, surname, patronymic, role_id FROM Users")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_name(name: str, surname: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, surname, patronymic, role_id FROM Users WHERE name = ? AND surname = ?", (name, surname))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None