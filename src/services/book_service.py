from repositories import book_repository, author_repository

def create_book(title: str, author_id: int, genre: str):
    if not title.strip() or not genre.strip():
        raise Exception("Название и жанр не могут быть пустыми")
    if not author_repository.get_by_id(author_id):
        raise Exception("Автор с таким ID не существует")
    book_repository.create(title, author_id, genre)

def get_all():
    return book_repository.get_all()

def update_book(book_id: int, title: str, author_id: int, genre: str):
    if not book_repository.get_by_id(book_id):
        raise Exception("Книга не найдена")
    if not author_repository.get_by_id(author_id):
        raise Exception("Автор с таким ID не существует")
    book_repository.update(book_id, title, author_id, genre)

def delete_book(book_id: int):
    if not book_repository.get_by_id(book_id):
        raise Exception("Книга не найдена")
    book_repository.delete(book_id)

def search_books(title: str):
    if not title.strip():
        raise Exception("Строка поиска пуста")
    return book_repository.search_by_title(title)