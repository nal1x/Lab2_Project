from services import author_service, book_service, user_service, booking_service

def admin_authors_menu():
    while True:
        print("\n--- Авторы ---")
        print("1. Добавить\n2. Все авторы\n3. Обновить\n4. Удалить\n0. Назад")
        c = input("Выбор: ")
        if c == "1":
            try:
                author_service.create_author(input("Имя: "), input("Фамилия: "), input("Отчество: ") or None)
                print("Успех")
            except Exception as e: print(e)
        elif c == "2":
            for a in author_service.get_all(): print(f"[{a.author_id}] {a.surname} {a.name}")
        elif c == "3":
            try:
                author_service.update_author(int(input("ID: ")), input("Имя: "), input("Фамилия: "), input("Отчество: ") or None)
                print("Успех")
            except Exception as e: print(e)
        elif c == "4":
            try:
                author_service.delete_author(int(input("ID: ")))
                print("Успех")
            except Exception as e: print(e)
        elif c == "0": break

def admin_books_menu():
    while True:
        print("\n--- Книги ---")
        print("1. Добавить\n2. Все книги\n3. Поиск книги\n4. Обновить\n5. Удалить\n0. Назад")
        c = input("Выбор: ")
        if c == "1":
            try:
                book_service.create_book(input("Название: "), int(input("ID автора: ")), input("Жанр: "))
                print("Успех")
            except Exception as e: print(e)
        elif c == "2":
            for b in book_service.get_all(): print(f"[{b.book_id}] {b.title}")
        elif c == "3":
            try:
                title = input("Введите название для поиска: ")
                books = book_service.search_books(title)
                if not books: print("Ничего не найдено")
                for b in books: print(f"[{b.book_id}] {b.title}")
            except Exception as e: print(e)
        elif c == "4":
            try:
                book_service.update_book(int(input("ID: ")), input("Название: "), int(input("ID автора: ")), input("Жанр: "))
                print("Успех")
            except Exception as e: print(e)
        elif c == "5":
            try:
                book_service.delete_book(int(input("ID: ")))
                print("Успех")
            except Exception as e: print(e)
        elif c == "0": break

def admin_users_menu():
    while True:
        print("\n--- Пользователи ---")
        print("1. Добавить\n2. Все\n3. Обновить\n4. Удалить\n0. Назад")
        c = input("Выбор: ")
        if c == "1":
            try:
                user_service.create_user(input("Имя: "), input("Фамилия: "), input("Отчество: ") or None, int(input("Роль (1-Админ,2-Читатель): ")), input("Логин: "), input("Пароль: "))
                print("Успех")
            except Exception as e: print(e)
        elif c == "2":
            for u in user_service.get_all(): print(f"[{u.user_id}] {u.login} (Роль: {u.role_id})")
        elif c == "3":
            try:
                user_service.update_user(int(input("ID: ")), input("Имя: "), input("Фамилия: "), input("Отчество: ") or None, int(input("Роль: ")), input("Логин: "), input("Пароль: "))
                print("Успех")
            except Exception as e: print(e)
        elif c == "4":
            try:
                user_service.delete_user(int(input("ID: ")))
                print("Успех")
            except Exception as e: print(e)
        elif c == "0": break

def admin_bookings_menu():
    while True:
        print("\n--- Бронирования ---")
        print("1. Добавить\n2. Все\n3. Обновить\n4. Удалить\n0. Назад")
        c = input("Выбор: ")
        if c == "1":
            try:
                booking_service.create_booking(int(input("ID юзера: ")), int(input("ID книги: ")), input("Начало: "), input("Конец: "))
                print("Успех")
            except Exception as e: print(e)
        elif c == "2":
            for b in booking_service.get_all(): print(f"[{b.booking_id}] Юзер {b.user_id}, Книга {b.book_id}")
        elif c == "3":
            try:
                booking_service.update_booking(int(input("ID: ")), int(input("ID юзера: ")), int(input("ID книги: ")), input("Начало: "), input("Конец: "))
                print("Успех")
            except Exception as e: print(e)
        elif c == "4":
            try:
                booking_service.delete_booking(int(input("ID: ")))
                print("Успех")
            except Exception as e: print(e)
        elif c == "0": break

def admin_menu(user):
    while True:
        print(f"\n===== АДМИН ({user.login}) =====")
        print("1. Авторы\n2. Книги\n3. Пользователи\n4. Бронирования\n0. Выход")
        c = input("Выбор: ")
        if c == "1": admin_authors_menu()
        elif c == "2": admin_books_menu()
        elif c == "3": admin_users_menu()
        elif c == "4": admin_bookings_menu()
        elif c == "0": break

def reader_menu(user):
    while True:
        print(f"\n===== ЧИТАТЕЛЬ ({user.login}) =====")
        print("1. Список всех книг\n2. Найти книгу\n3. Забронировать книгу\n4. Мои бронирования\n0. Выход")
        c = input("Выбор: ")
        if c == "1":
            for b in book_service.get_all(): print(f"[{b.book_id}] {b.title} (Жанр: {b.genre})")
        elif c == "2":
            title = input("Введите название для поиска: ")
            try:
                books = book_service.search_books(title)
                if not books: print("Ничего не найдено")
                for b in books: print(f"[{b.book_id}] {b.title}")
            except Exception as e: print(e)
        elif c == "3":
            try:
                book_id = int(input("Введите ID книги: "))
                start_date = input("Дата начала (ДД.ММ.ГГГГ): ")
                end_date = input("Дата окончания (ДД.ММ.ГГГГ): ")
                booking_service.create_booking(user.user_id, book_id, start_date, end_date)
                print("Успех: Книга забронирована!")
            except ValueError:
                print("Ошибка: ID книги должен быть числом")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif c == "4":
            bkgs = booking_service.get_by_user(user.user_id)
            if not bkgs:
                print("У вас нет активных бронирований.")
            for b in bkgs: print(f"Книга ID {b.book_id} | {b.booking_start_date} - {b.end_date_of_booking}")
        elif c == "0": break