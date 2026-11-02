from repositories import booking_repository


def create_booking(user_id: int, book_id: int, start_date: str, end_date: str):
    if user_id <= 0:
        raise Exception("ID пользователя должен быть положительным числом")
    if book_id <= 0:
        raise Exception("ID книги должен быть положительным числом")
    if not start_date.strip():
        raise Exception("Дата начала бронирования не может быть пустой")
    if not end_date.strip():
        raise Exception("Дата окончания бронирования не может быть пустой")

    booking_repository.create(user_id, book_id, start_date, end_date)