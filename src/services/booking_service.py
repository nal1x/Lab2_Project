from datetime import datetime
from repositories import booking_repository, user_repository, book_repository


def _parse_and_validate_dates(start_str: str, end_str: str) -> tuple[datetime, datetime]:
    fmt = "%d.%m.%Y"
    try:
        start_dt = datetime.strptime(start_str, fmt)
        end_dt = datetime.strptime(end_str, fmt)
    except ValueError:
        raise Exception("Неверный формат даты. Используйте ДД.ММ.ГГГГ")
    if start_dt > end_dt:
        raise Exception("Дата начала не может быть позже даты окончания")
    return start_dt, end_dt


def _check_dates_overlap(start1: datetime, end1: datetime, start2_str: str, end2_str: str) -> bool:
    fmt = "%d.%m.%Y"
    s2 = datetime.strptime(start2_str, fmt)
    e2 = datetime.strptime(end2_str, fmt)
    return max(start1, s2) <= min(end1, e2)


def create_booking(user_id: int, book_id: int, start_date: str, end_date: str):
    if not start_date.strip() or not end_date.strip():
        raise Exception("Даты не могут быть пустыми")
    start_dt, end_dt = _parse_and_validate_dates(start_date, end_date)
    user = user_repository.get_by_id(user_id)
    if not user:
        raise Exception("Пользователь не найден")
    if user.role_id != 2:
        raise Exception("Бронировать книги могут только читатели")
    if not book_repository.get_by_id(book_id):
        raise Exception("Книга не найдена")
    existing = booking_repository.get_by_book(book_id)
    for b in existing:
        if _check_dates_overlap(start_dt, end_dt, b.booking_start_date, b.end_date_of_booking):
            raise Exception("Эта книга уже забронирована на выбранные даты")
    booking_repository.create(user_id, book_id, start_date, end_date)


def get_all():
    return booking_repository.get_all()


def get_by_user(user_id: int):
    return booking_repository.get_by_user(user_id)


def update_booking(booking_id: int, user_id: int, book_id: int, start_date: str, end_date: str):
    if not booking_repository.get_by_id(booking_id):
        raise Exception("Бронирование с таким ID не найдено")

    user = user_repository.get_by_id(user_id)
    if not user:
        raise Exception("Пользователь не найден")
    if user.role_id != 2:
        raise Exception("Бронировать книги могут только читатели")

    if not book_repository.get_by_id(book_id):
        raise Exception("Книга не найдена")

    if not start_date.strip() or not end_date.strip():
        raise Exception("Даты не могут быть пустыми")

    start_dt, end_dt = _parse_and_validate_dates(start_date, end_date)

    existing = booking_repository.get_by_book(book_id)
    for b in existing:
        if b.booking_id != booking_id:
            if _check_dates_overlap(start_dt, end_dt, b.booking_start_date, b.end_date_of_booking):
                raise Exception("Эта книга уже забронирована на выбранные даты другим бронированием")

    booking_repository.update(booking_id, user_id, book_id, start_date, end_date)


def delete_booking(booking_id: int):
    if not booking_repository.get_by_id(booking_id):
        raise Exception("Бронирование не найдено")
    booking_repository.delete(booking_id)