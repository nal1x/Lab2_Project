from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    name: str
    surname: str
    patronymic: str | None
    role_id: int
    login: str
    password: str