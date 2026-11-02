from dataclasses import dataclass

@dataclass
class Booking:
    booking_id: int
    user_id: int
    book_id: int
    booking_start_date: str
    end_date_of_booking: str