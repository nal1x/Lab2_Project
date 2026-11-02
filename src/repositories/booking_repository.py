from database.database import get_connection
from models.booking import Booking

def _map(row) -> Booking:
    return Booking(*row)

def create(user_id: int, book_id: int, booking_start_date: str, end_date_of_booking: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Bookings(user_id, book_id, booking_start_date, end_date_of_booking) VALUES (?, ?, ?, ?)", (user_id, book_id, booking_start_date, end_date_of_booking))
    conn.commit()
    conn.close()

def get_all() -> list[Booking]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT booking_id, user_id, book_id, booking_start_date, end_date_of_booking FROM Bookings")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(booking_id: int) -> Booking | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT booking_id, user_id, book_id, booking_start_date, end_date_of_booking FROM Bookings WHERE booking_id = ?", (booking_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_user(user_id: int) -> list[Booking]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT booking_id, user_id, book_id, booking_start_date, end_date_of_booking FROM Bookings WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update(booking_id: int, user_id: int, book_id: int, booking_start_date: str, end_date_of_booking: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Bookings SET user_id = ?, book_id = ?, booking_start_date = ?, end_date_of_booking = ? WHERE booking_id = ?", (user_id, book_id, booking_start_date, end_date_of_booking, booking_id))
    conn.commit()
    conn.close()

def delete(booking_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Bookings WHERE booking_id = ?", (booking_id,))
    conn.commit()
    conn.close()

def get_by_book(book_id: int) -> list[Booking]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT booking_id, user_id, book_id, booking_start_date, end_date_of_booking FROM Bookings WHERE book_id = ?", (book_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]