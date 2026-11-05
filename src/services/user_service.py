import hashlib
import os
from repositories import user_repository, role_repository, booking_repository

def _hash_password(password: str, salt: str = None) -> str:
    if salt is None:
        salt = os.urandom(16).hex()
    h = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return f"{salt}${h}"

def create_user(name: str, surname: str, patronymic: str | None, role_id: int, login: str, password: str):
    name = name.strip()
    surname = surname.strip()
    patronymic = patronymic.strip() if patronymic else None
    login = login.strip()
    password = password.strip()
    if not name or not surname or not login or not password:
        raise Exception("Поля имя, фамилия, логин и пароль обязательны")
    if len(password) < 4:
        raise Exception("Пароль должен содержать не менее 4 символов")
    if not role_repository.get_by_id(role_id):
        raise Exception("Указанная роль не существует")
    if user_repository.get_by_login(login):
        raise Exception("Логин уже занят")
    user_repository.create(name, surname, patronymic, role_id, login, _hash_password(password))

def get_all():
    return user_repository.get_all()

def authenticate(login_val: str, password_val: str):
    login_val = login_val.strip()
    password_val = password_val.strip()
    user = user_repository.get_by_login(login_val)
    if not user:
        raise Exception("Неверный логин или пароль")
    try:
        salt, _ = user.password.split('$')
    except ValueError:
        raise Exception("Ошибка формата пароля в БД")
    if user.password != _hash_password(password_val, salt):
        raise Exception("Неверный логин или пароль")
    return user

def update_user(user_id: int, name: str, surname: str, patronymic: str | None, role_id: int, login: str, password: str):
    if not user_repository.get_by_id(user_id):
        raise Exception("Пользователь не найден")
    name = name.strip()
    surname = surname.strip()
    patronymic = patronymic.strip() if patronymic else None
    login = login.strip()
    password = password.strip()
    if not name or not surname or not login or not password:
        raise Exception("Поля имя, фамилия, логин и пароль обязательны")
    if len(password) < 4:
        raise Exception("Пароль должен содержать не менее 4 символов")
    if not role_repository.get_by_id(role_id):
        raise Exception("Указанная роль не существует")
    existing_user = user_repository.get_by_login(login)
    if existing_user and existing_user.user_id != user_id:
        raise Exception("Логин уже занят")
    user_repository.update(user_id, name, surname, patronymic, role_id, login, _hash_password(password))

def delete_user(user_id: int):
    if not user_repository.get_by_id(user_id):
        raise Exception("Пользователь не найден")
    bookings = booking_repository.get_by_user(user_id)
    if bookings:
        raise Exception("Невозможно удалить пользователя, у которого есть бронирования")
    user_repository.delete(user_id)