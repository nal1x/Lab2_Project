from services import user_service

def login():
    print("\n===== АВТОРИЗАЦИЯ =====")
    login_val = input("Логин: ")
    password_val = input("Пароль: ")
    try:
        return user_service.authenticate(login_val, password_val)
    except Exception as e:
        print(f"Ошибка: {e}")
        return None