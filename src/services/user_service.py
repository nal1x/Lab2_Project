from repositories import user_repository


def create_user(name: str, surname: str, patronymic: str | None, role_id: int):
    if not name.strip():
        raise Exception("Имя не может быть пустым")
    if not surname.strip():
        raise Exception("Фамилия не может быть пустой")
    if role_id not in [1, 2]:
        raise Exception("Неверная роль! В базе есть только 1 (Администратор) и 2 (Читатель)")

    user_repository.create(name, surname, patronymic, role_id)


def authenticate(name: str, surname: str):
    if not name.strip() or not surname.strip():
        raise Exception("Имя и фамилия не могут быть пустыми")

    user = user_repository.get_by_name(name, surname)
    if not user:
        raise Exception("Пользователь с такими данными не найден")

    return user