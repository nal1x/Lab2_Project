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
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
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

INSERT INTO Roles (name) VALUES ('Администратор'), ('Читатель');

INSERT INTO Authors (name, surname, patronymic) VALUES ('Федор', 'Достоевский', 'Михайлович'), ('Лев', 'Толстой', 'Николаевич');

INSERT INTO Users (name, surname, patronymic, role_id, login, password) VALUES
('Алексей', 'Смирнов', '', 1, 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'),
('Иван', 'Иванов', 'Иванович', 2, 'ivan', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'),
('Анна', 'Петрова', 'Сергеевна', 2, 'anna', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4');

INSERT INTO Books (title, author_id, genre) VALUES ('Преступление и наказание', 1, 'Роман'), ('Война и мир', 2, 'Роман-эпопея');

INSERT INTO Bookings (user_id, book_id, booking_start_date, end_date_of_booking) VALUES (2, 1, '25.10.2026', '08.11.2026'), (3, 2, '26.10.2026', '09.11.2026');
