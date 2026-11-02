from repositories import book_repository


def create_book(title: str, author_id: int, genre: str):
    if not title.strip():
        raise Exception("Название книги не может быть пустым")
    if not genre.strip():
        raise Exception("Жанр не может быть пустым")
    if author_id <= 0:
        raise Exception("ID автора должен быть положительным числом")

    book_repository.create(title, author_id, genre)