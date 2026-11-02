from database.database import get_connection
from models.booking import Booking

def _map(row) -> Booking:
    return Booking(*row)

def create(user_id: int, book_id: int, booking_start_date: str, end_date_of_booking: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Bookings(user_id, book_id, booking_start_date, end_date_of_booking)
        VALUES (?, ?, ?, ?)
    """, (user_id, book_id, booking_start_date, end_date_of_booking))
    conn.commit()
    conn.close()

def get_all() -> list[Booking]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT booking_id, user_id, book_id, booking_start_date, end_date_of_booking FROM Bookings")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]