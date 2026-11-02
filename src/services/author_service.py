from repositories import author_repository

def create_author(name: str, surname: str, patronymic: str | None):
    if not name.strip() or not surname.strip():
        raise Exception("Имя и фамилия не могут быть пустыми")
    if author_repository.get_exact(name, surname, patronymic):
        raise Exception("Такой автор уже существует")
    author_repository.create(name, surname, patronymic)

def get_all():
    return author_repository.get_all()

def update_author(author_id: int, name: str, surname: str, patronymic: str | None):
    if not name.strip() or not surname.strip():
        raise Exception("Имя и фамилия не могут быть пустыми")
    if not author_repository.get_by_id(author_id):
        raise Exception("Автор не найден")
    existing = author_repository.get_exact(name, surname, patronymic)
    if existing and existing.author_id != author_id:
        raise Exception("Такой автор уже существует")
    author_repository.update(author_id, name, surname, patronymic)

def delete_author(author_id: int):
    if not author_repository.get_by_id(author_id):
        raise Exception("Автор не найден")
    author_repository.delete(author_id)