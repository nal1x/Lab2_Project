from services import author_service, book_service, user_service, booking_service
from repositories import author_repository, book_repository, user_repository, booking_repository


def authors_menu():
    while True:
        print("\n===== Меню авторов =====")
        print("1. Добавить автора")
        print("2. Показать всех авторов")
        print("0. Назад")
        choice = input("Выберите действие: ")
        if choice == "1":
            name = input("Введите имя: ")
            surname = input("Введите фамилию: ")
            patronymic = input("Введите отчество (или оставьте пустым): ") or None
            try:
                author_service.create_author(name, surname, patronymic)
                print("Успех: Автор успешно добавлен!")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "2":
            authors = author_repository.get_all()
            if not authors:
                print("Список авторов пуст.")
            for a in authors:
                print(f"[{a.author_id}] {a.surname} {a.name} {a.patronymic or ''}")
        elif choice == "0":
            break
        else:
            print("Неверный ввод.")


def books_menu():
    while True:
        print("\n===== Меню книг =====")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("0. Назад")
        choice = input("Выберите действие: ")
        if choice == "1":
            title = input("Введите название книги: ")
            author_id = input("Введите ID автора (число): ")
            genre = input("Введите жанр: ")
            try:
                book_service.create_book(title, int(author_id), genre)
                print("Успех: Книга добавлена!")
            except ValueError:
                print("Ошибка: ID автора должно быть числом!")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "2":
            books = book_repository.get_all()
            if not books:
                print("Список книг пуст.")
            for b in books:
                print(f"[{b.book_id}] '{b.title}' (Жанр: {b.genre}, ID автора: {b.author_id})")
        elif choice == "0":
            break
        else:
            print("Неверный ввод.")


def users_menu():
    while True:
        print("\n===== Меню пользователей =====")
        print("1. Добавить пользователя")
        print("2. Показать всех пользователей")
        print("0. Назад")
        choice = input("Выберите действие: ")
        if choice == "1":
            name = input("Введите имя: ")
            surname = input("Введите фамилию: ")
            patronymic = input("Введите отчество (или пусто): ") or None
            role_id = input("Введите ID роли (1 - Админ, 2 - Читатель): ")
            try:
                user_service.create_user(name, surname, patronymic, int(role_id))
                print("Успех: Пользователь добавлен!")
            except ValueError:
                print("Ошибка: Роль должна быть числом!")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "2":
            users = user_repository.get_all()
            if not users:
                print("Список пользователей пуст.")
            for u in users:
                role_name = "Админ" if u.role_id == 1 else "Читатель"
                print(f"[{u.user_id}] {u.surname} {u.name} - Роль: {role_name}")
        elif choice == "0":
            break
        else:
            print("Неверный ввод.")


def bookings_menu():
    while True:
        print("\n===== Меню бронирований =====")
        print("1. Добавить бронирование")
        print("2. Показать все бронирования")
        print("0. Назад")
        choice = input("Выберите действие: ")
        if choice == "1":
            user_id = input("Введите ID пользователя (число): ")
            book_id = input("Введите ID книги (число): ")
            start_date = input("Введите дату начала (например, 25.10.2026): ")
            end_date = input("Введите дату окончания (например, 08.11.2026): ")
            try:
                booking_service.create_booking(int(user_id), int(book_id), start_date, end_date)
                print("Успех: Бронирование добавлено!")
            except ValueError:
                print("Ошибка: ID пользователя и ID книги должны быть числами!")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "2":
            bookings = booking_repository.get_all()
            if not bookings:
                print("Список бронирований пуст.")
            for bk in bookings:
                print(
                    f"[{bk.booking_id}] Пользователь ID: {bk.user_id}, Книга ID: {bk.book_id} | {bk.booking_start_date} - {bk.end_date_of_booking}")
        elif choice == "0":
            break
        else:
            print("Неверный ввод.")


def admin_menu(user):
    while True:
        print(f"\n===== ПАНЕЛЬ АДМИНИСТРАТОРА ({user.name} {user.surname}) =====")
        print("1. Работа с авторами")
        print("2. Работа с книгами")
        print("3. Работа с пользователями")
        print("4. Работа с бронированиями")
        print("0. Выход из аккаунта")
        choice = input("Выберите раздел: ")

        if choice == "1":
            authors_menu()
        elif choice == "2":
            books_menu()
        elif choice == "3":
            users_menu()
        elif choice == "4":
            bookings_menu()
        elif choice == "0":
            print("Выход из аккаунта...")
            break
        else:
            print("Неверный ввод.")


def reader_menu(user):
    while True:
        print(f"\n===== МЕНЮ ЧИТАТЕЛЯ ({user.name} {user.surname}) =====")
        print("1. Работа с книгами")
        print("2. Работа с бронированиями")
        print("0. Выход из аккаунта")
        choice = input("Выберите раздел: ")

        if choice == "1":
            books_menu()
        elif choice == "2":
            bookings_menu()
        elif choice == "0":
            print("Выход из аккаунта...")
            break
        else:
            print("Неверный ввод.")