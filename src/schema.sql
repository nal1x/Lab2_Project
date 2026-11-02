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

INSERT OR IGNORE INTO Users (user_id, name, surname, patronymic, role_id, login, password) VALUES
(1, 'Алексей', 'Смирнов', '', 1, 'admin', 'salt$63c0a5ea6c4cb71c77573f0896fa2c30045e7f1bf5de93b95ce7d432320b2241'),
(2, 'Иван', 'Иванов', 'Иванович', 2, 'ivan', 'salt$0c6eef9dd40e599e3a6c507c57659556db2908865c3b99eb01d1c5d3363e792c'),
(3, 'Анна', 'Петрова', 'Сергеевна', 2, 'anna', 'salt$0c6eef9dd40e599e3a6c507c57659556db2908865c3b99eb01d1c5d3363e792c');

INSERT OR IGNORE INTO Books (book_id, title, author_id, genre) VALUES (1, 'Преступление и наказание', 1, 'Роман'), (2, 'Война и мир', 2, 'Роман-эпопея');

INSERT OR IGNORE INTO Bookings (booking_id, user_id, book_id, booking_start_date, end_date_of_booking) VALUES (1, 2, 1, '25.10.2026', '08.11.2026'), (2, 3, 2, '26.10.2026', '09.11.2026');
