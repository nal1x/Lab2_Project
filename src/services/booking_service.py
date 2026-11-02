from datetime import datetime
from repositories import booking_repository, user_repository, book_repository

def _check_dates_overlap(start1: str, end1: str, start2: str, end2: str) -> bool:
    fmt = "%d.%m.%Y"
    try:
        s1, e1 = datetime.strptime(start1, fmt), datetime.strptime(end1, fmt)
        s2, e2 = datetime.strptime(start2, fmt), datetime.strptime(end2, fmt)
    except ValueError:
        raise Exception("Неверный формат даты. Используйте ДД.ММ.ГГГГ")
    if s1 > e1 or s2 > e2:
        raise Exception("Дата начала не может быть позже даты окончания")
    return max(s1, s2) <= min(e1, e2)

def create_booking(user_id: int, book_id: int, start_date: str, end_date: str):
    if not user_repository.get_by_id(user_id):
        raise Exception("Пользователь не найден")
    if not book_repository.get_by_id(book_id):
        raise Exception("Книга не найдена")
    if not start_date.strip() or not end_date.strip():
        raise Exception("Даты не могут быть пустыми")
    existing = booking_repository.get_by_book(book_id)
    for b in existing:
        if _check_dates_overlap(start_date, end_date, b.booking_start_date, b.end_date_of_booking):
            raise Exception("Эта книга уже забронирована на выбранные даты")
    booking_repository.create(user_id, book_id, start_date, end_date)

def get_all():
    return booking_repository.get_all()

def get_by_user(user_id: int):
    return booking_repository.get_by_user(user_id)

def update_booking(booking_id: int, user_id: int, book_id: int, start_date: str, end_date: str):
    if not booking_repository.get_by_id(booking_id):
        raise Exception("Бронирование не найдено")
    if not user_repository.get_by_id(user_id):
        raise Exception("Пользователь не найден")
    if not book_repository.get_by_id(book_id):
        raise Exception("Книга не найдена")
    existing = booking_repository.get_by_book(book_id)
    for b in existing:
        if b.booking_id != booking_id:
            if _check_dates_overlap(start_date, end_date, b.booking_start_date, b.end_date_of_booking):
                raise Exception("Эта книга уже забронирована на выбранные даты другим бронированием")
    booking_repository.update(booking_id, user_id, book_id, start_date, end_date)

def delete_booking(booking_id: int):
    if not booking_repository.get_by_id(booking_id):
        raise Exception("Бронирование не найдено")
    booking_repository.delete(booking_id)