from repositories import booking_repository, user_repository, book_repository

def create_booking(user_id: int, book_id: int, start_date: str, end_date: str):
    if not user_repository.get_by_id(user_id):
        raise Exception("Пользователь не найден")
    if not book_repository.get_by_id(book_id):
        raise Exception("Книга не найдена")
    if not start_date.strip() or not end_date.strip():
        raise Exception("Даты не могут быть пустыми")
    booking_repository.create(user_id, book_id, start_date, end_date)

def get_all():
    return booking_repository.get_all()

def get_by_user(user_id: int):
    return booking_repository.get_by_user(user_id)

def update_booking(booking_id: int, user_id: int, book_id: int, start_date: str, end_date: str):
    if not booking_repository.get_by_id(booking_id):
        raise Exception("Бронирование не найдено")
    booking_repository.update(booking_id, user_id, book_id, start_date, end_date)

def delete_booking(booking_id: int):
    if not booking_repository.get_by_id(booking_id):
        raise Exception("Бронирование не найдено")
    booking_repository.delete(booking_id)