import hashlib
from repositories import user_repository, role_repository

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_user(name: str, surname: str, patronymic: str | None, role_id: int, login: str, password: str):
    if not name.strip() or not surname.strip() or not login.strip() or not password.strip():
        raise Exception("Поля имя, фамилия, логин и пароль обязательны")
    if not role_repository.get_by_id(role_id):
        raise Exception("Указанная роль не существует")
    if user_repository.get_by_login(login):
        raise Exception("Логин уже занят")
    user_repository.create(name, surname, patronymic, role_id, login, _hash_password(password))

def get_all():
    return user_repository.get_all()

def authenticate(login_val: str, password_val: str):
    user = user_repository.get_by_login(login_val)
    if not user or user.password != _hash_password(password_val):
        raise Exception("Неверный логин или пароль")
    return user

def update_user(user_id: int, name: str, surname: str, patronymic: str | None, role_id: int, login: str, password: str):
    if not user_repository.get_by_id(user_id):
        raise Exception("Пользователь не найден")
    if not role_repository.get_by_id(role_id):
        raise Exception("Указанная роль не существует")
    existing_user = user_repository.get_by_login(login)
    if existing_user and existing_user.user_id != user_id:
        raise Exception("Логин уже занят")
    user_repository.update(user_id, name, surname, patronymic, role_id, login, _hash_password(password))

def delete_user(user_id: int):
    if not user_repository.get_by_id(user_id):
        raise Exception("Пользователь не найден")
    user_repository.delete(user_id)