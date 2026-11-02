from dataclasses import dataclass

@dataclass
class Book:
    book_id: int
    title: str
    author_id: int
    genre: str