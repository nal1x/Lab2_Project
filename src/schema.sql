CREATE TABLE IF NOT EXISTS Roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT
);

CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT,
    role_id INTEGER NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES Roles (role_id)
);

CREATE TABLE IF NOT EXISTS Books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    genre TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES Authors (author_id)
);

CREATE TABLE IF NOT EXISTS Bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    booking_start_date TEXT NOT NULL,
    end_date_of_booking TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    FOREIGN KEY (book_id) REFERENCES Books (book_id)
);

INSERT OR IGNORE INTO Roles (role_id, name) VALUES (1, 'Администратор'), (2, 'Читатель');

INSERT OR IGNORE INTO Authors (author_id, name, surname, patronymic) VALUES (1, 'Федор', 'Достоевский', 'Михайлович'), (2, 'Лев', 'Толстой', 'Николаевич');

INSERT OR IGNORE INTO Books (book_id, title, author_id, genre) VALUES (1, 'Преступление и наказание', 1, 'Роман'), (2, 'Война и мир', 2, 'Роман-эпопея');
