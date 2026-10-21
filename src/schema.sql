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
    name TEXT NOT NULL
);

CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES Roles (role_id)
);

CREATE TABLE Books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES Authors (author_id)
);

CREATE TABLE Bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    date TEXT,
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    FOREIGN KEY (book_id) REFERENCES Books (book_id)
);

INSERT INTO Roles (name) VALUES ('Администратор'), ('Читатель');
INSERT INTO Authors (name) VALUES ('Ф.М. Достоевский'), ('Л.Н. Толстой');
INSERT INTO Users (username, role_id) VALUES ('Иван', 2), ('Анна', 2);
INSERT INTO Books (title, author_id) VALUES ('Преступление и наказание', 1), ('Война и мир', 2);
INSERT INTO Bookings (user_id, book_id, date) VALUES (1, 1, '25.10.2026'), (2, 2, '26.10.2026');