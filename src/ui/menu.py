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
                raw_id = input("ID: ")
                if not raw_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                author_service.update_author(int(raw_id), input("Имя: "), input("Фамилия: "), input("Отчество: ") or None)
                print("Успех")
            except Exception as e: print(e)
        elif c == "4":
            try:
                raw_id = input("ID: ")
                if not raw_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                author_service.delete_author(int(raw_id))
                print("Успех")
            except Exception as e: print(e)
        elif c == "0": break
        else:
            print("неверный формат ввода данных")

def admin_books_menu():
    while True:
        print("\n--- Книги ---")
        print("1. Добавить\n2. Все книги\n3. Поиск книги\n4. Обновить\n5. Удалить\n0. Назад")
        c = input("Выбор: ")
        if c == "1":
            try:
                raw_author_id = input("ID автора: ")
                if not raw_author_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                book_service.create_book(input("Название: "), int(raw_author_id), input("Жанр: "))
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
                raw_id = input("ID: ")
                if not raw_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                raw_author_id = input("ID автора: ")
                if not raw_author_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                book_service.update_book(int(raw_id), input("Название: "), int(raw_author_id), input("Жанр: "))
                print("Успех")
            except Exception as e: print(e)
        elif c == "5":
            try:
                raw_id = input("ID: ")
                if not raw_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                book_service.delete_book(int(raw_id))
                print("Успех")
            except Exception as e: print(e)
        elif c == "0": break
        else:
            print("неверный формат ввода данных")

def admin_users_menu():
    while True:
        print("\n--- Пользователи ---")
        print("1. Добавить\n2. Все\n3. Обновить\n4. Удалить\n0. Назад")
        c = input("Выбор: ")
        if c == "1":
            try:
                raw_role_id = input("Роль (1-Админ,2-Читатель): ")
                if not raw_role_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                user_service.create_user(input("Имя: "), input("Фамилия: "), input("Отчество: ") or None, int(raw_role_id), input("Логин: "), input("Пароль: "))
                print("Успех")
            except Exception as e: print(e)
        elif c == "2":
            for u in user_service.get_all(): print(f"[{u.user_id}] {u.login} (Роль: {u.role_id})")
        elif c == "3":
            try:
                raw_id = input("ID: ")
                if not raw_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                raw_role_id = input("Роль: ")
                if not raw_role_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                user_service.update_user(int(raw_id), input("Имя: "), input("Фамилия: "), input("Отчество: ") or None, int(raw_role_id), input("Логин: "), input("Пароль: "))
                print("Успех")
            except Exception as e: print(e)
        elif c == "4":
            try:
                raw_id = input("ID: ")
                if not raw_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                user_service.delete_user(int(raw_id))
                print("Успех")
            except Exception as e: print(e)
        elif c == "0": break
        else:
            print("неверный формат ввода данных")

def admin_bookings_menu():
    while True:
        print("\n--- Бронирования ---")
        print("1. Добавить\n2. Все\n3. Обновить\n4. Удалить\n0. Назад")
        c = input("Выбор: ")
        if c == "1":
            try:
                raw_user_id = input("ID юзера: ")
                if not raw_user_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                raw_book_id = input("ID книги: ")
                if not raw_book_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                booking_service.create_booking(int(raw_user_id), int(raw_book_id), input("Начало: "), input("Конец: "))
                print("Успех")
            except Exception as e: print(e)
        elif c == "2":
            for b in booking_service.get_all(): print(f"[{b.booking_id}] Юзер {b.user_id}, Книга {b.book_id}")
        elif c == "3":
            try:
                raw_id = input("ID: ")
                if not raw_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                raw_user_id = input("ID юзера: ")
                if not raw_user_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                raw_book_id = input("ID книги: ")
                if not raw_book_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                booking_service.update_booking(int(raw_id), int(raw_user_id), int(raw_book_id), input("Начало: "), input("Конец: "))
                print("Успех")
            except Exception as e: print(e)
        elif c == "4":
            try:
                raw_id = input("ID: ")
                if not raw_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                booking_service.delete_booking(int(raw_id))
                print("Успех")
            except Exception as e: print(e)
        elif c == "0": break
        else:
            print("неверный формат ввода данных")

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
        else:
            print("неверный формат ввода данных")

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
                raw_book_id = input("Введите ID книги: ")
                if not raw_book_id.isdigit():
                    print("неверный формат ввода данных")
                    continue
                start_date = input("Дата начала (ДД.ММ.ГГГГ): ")
                end_date = input("Дата окончания (ДД.ММ.ГГГГ): ")
                booking_service.create_booking(user.user_id, int(raw_book_id), start_date, end_date)
                print("Успех: Книга забронирована!")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif c == "4":
            bkgs = booking_service.get_by_user(user.user_id)
            if not bkgs:
                print("У вас нет активных бронирований.")
            for b in bkgs: print(f"Книга ID {b.book_id} | {b.booking_start_date} - {b.end_date_of_booking}")
        elif c == "0": break
        else:
            print("неверный формат ввода данных")