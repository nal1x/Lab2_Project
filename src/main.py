from database.database import init_db
from ui.auth import login
from ui.menu import admin_menu, reader_menu
from export_data import auto_export

if __name__ == "__main__":
    init_db()
    auto_export("Books")

    while True:
        user = login()

        if user:
            if user.role_id == 1:
                admin_menu(user)
            elif user.role_id == 2:
                reader_menu(user)

        if input("\nВойти снова? (1-да, 0-нет): ") == "0":
            break
