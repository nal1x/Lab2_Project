DROP TABLE IF EXISTS Bookings;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS Roles;

CREATE TABLE Roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE Authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT
);

CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES Roles (role_id)
);

CREATE TABLE Books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    genre TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES Authors (author_id)
);

CREATE TABLE Bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    booking_start_date TEXT NOT NULL,
    end_date_of_booking TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    FOREIGN KEY (book_id) REFERENCES Books (book_id)
);

INSERT INTO Roles (name) VALUES
('Администратор'),
('Читатель');

INSERT INTO Authors (name, surname, patronymic) VALUES
('Федор', 'Достоевский', 'Михайлович'),
('Лев', 'Толстой', 'Николаевич');

INSERT INTO Users (name, surname, patronymic, role_id) VALUES
('Иван', 'Иванов', 'Иванович', 2),
('Анна', 'Петрова', 'Сергеевна', 2);

INSERT INTO Books (title, author_id, genre) VALUES
('Преступление и наказание', 1, 'Роман'),
('Война и мир', 2, 'Роман-эпопея');

INSERT INTO Bookings (user_id, book_id, booking_start_date, end_date_of_booking) VALUES
(1, 1, '25.10.2026', '08.11.2026'),
(2, 2, '26.10.2026', '09.11.2026');
