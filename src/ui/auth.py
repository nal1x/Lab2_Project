from services import user_service


def login():
    print("\n===== АВТОРИЗАЦИЯ =====")
    name = input("Введите ваше имя: ")
    surname = input("Введите вашу фамилию: ")

    try:
        user = user_service.authenticate(name, surname)
        return user
    except Exception as e:
        print(f"Ошибка входа: {e}")
        return None