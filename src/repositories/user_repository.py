from database.database import get_connection
from models.user import User

def _map(row) -> User:
    return User(*row)

def create(name: str, surname: str, patronymic: str | None, role_id: int, login: str, password: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Users(name, surname, patronymic, role_id, login, password) VALUES (?, ?, ?, ?, ?, ?)", (name, surname, patronymic, role_id, login, password))
    conn.commit()
    conn.close()

def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, surname, patronymic, role_id, login, password FROM Users")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, surname, patronymic, role_id, login, password FROM Users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, surname, patronymic, role_id, login, password FROM Users WHERE login = ?", (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def update(user_id: int, name: str, surname: str, patronymic: str | None, role_id: int, login: str, password: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Users SET name = ?, surname = ?, patronymic = ?, role_id = ?, login = ?, password = ? WHERE user_id = ?", (name, surname, patronymic, role_id, login, password, user_id))
    conn.commit()
    conn.close()

def delete(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()