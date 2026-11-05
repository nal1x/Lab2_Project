from repositories import author_repository, book_repository

def create_author(name: str, surname: str, patronymic: str | None):
    name = name.strip()
    surname = surname.strip()
    patronymic = patronymic.strip() if patronymic else None
    if not name or not surname:
        raise Exception("Имя и фамилия не могут быть пустыми")
    if author_repository.get_exact(name, surname, patronymic):
        raise Exception("Такой автор уже существует")
    author_repository.create(name, surname, patronymic)

def get_all():
    return author_repository.get_all()

def update_author(author_id: int, name: str, surname: str, patronymic: str | None):
    if not author_repository.get_by_id(author_id):
        raise Exception("Автор не найден")
    name = name.strip()
    surname = surname.strip()
    patronymic = patronymic.strip() if patronymic else None
    if not name or not surname:
        raise Exception("Имя и фамилия не могут быть пустыми")
    existing = author_repository.get_exact(name, surname, patronymic)
    if existing and existing.author_id != author_id:
        raise Exception("Такой автор уже существует")
    author_repository.update(author_id, name, surname, patronymic)

def delete_author(author_id: int):
    if not author_repository.get_by_id(author_id):
        raise Exception("Автор не найден")
    books = book_repository.get_by_author(author_id)
    if books:
        raise Exception("Невозможно удалить автора, у которого есть книги")
    author_repository.delete(author_id)