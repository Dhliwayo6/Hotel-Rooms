import csv
import sys
import calendar
import getpass
import smtplib
import uuid
import re
from passwords import pwd
from datetime import date
from prettytable import PrettyTable

table = PrettyTable(["Room Number", "Room Type", "Price"])


def main():

    print("Welcome to the Grand Ladora \nPlease register before making a booking")

    print()

    while True:

        print("1.Register \n2. Login")

        entry = input("Choose an option: ")

        if entry == "1" or entry == "Register":

            name = input("Please enter your name: ").capitalize().strip()

            surname = input("Please enter your surname: ").capitalize().strip()

            email = input("Please enter your email adddress: ").strip()
            print()

            if not is_valid_email(email):
                print(f"{email} not a valid email address, Please try again!\n")
                continue

            register(name, surname, email)

            print(
                f"Guest {name.capitalize()} {surname} successfully registered\nProceed to login now"
            )

        elif entry == "2" or entry == "Login":
            login_name = input("Enter your name: ").capitalize().strip()

            login_email = input("Enter your email: ").strip()

            if not is_valid_email(login_email):
                print(f"{login_email} not a valid email address, Please try again!\n")
                continue

            if client_login(login_name, login_email):
                print("Login successful!")
                print()
                break
            else:
                print("Login failed! \nPlease check your details or register")
                print()

        else:
            print("Invalid selection")

    current_date = date.today()

    current_date = str(current_date)

    year, month, day = current_date.split("-")

    while True:

        try:

            print(calendar.month(int(year), int(month)))
            print()

            check_in = int(input("Please choose a check-in date: "))
            print()

            print(calendar.month(int(year), int(month)))
            print()

            check_out = int(input("Please choose a check-out date: "))
            print()

            if check_in == check_out:
                print(
                    "You cannot check-out on the same day you check-in, Please try again!"
                )
                print()
                continue
            break

        except ValueError:

            print("Not a valid date, try again.")

    available = open_available_rooms()

    unavailable = open_unavailable_rooms()

    print("These are the available rooms to book")

    available_rooms_display = show_available_rooms(available, unavailable)

    for room in available_rooms_display:
        table.add_row([room["number"], room["type"], room["price"]])

    print(table)

    number = input("Pick a room number: ")

    price = room_price(available, number)

    check_in_date = year + "-" + month + "-" + str(check_in)
    check_out_date = year + "-" + month + "-" + str(check_out)

    nights_spent = check_out - check_in

    total_cost = stay_cost(nights_spent, price)

    print(f"Your stay for {nights_spent} night(s) is ZAR {total_cost:,.2f}")

    book_room(number, check_in_date, check_out_date, login_name, login_email)

    HOST = "smtp.gmail.com"

    PORT = 587

    from_email = "thegrandladorahotel@gmail.com"

    to_email = login_email

    password = pwd

    for room in available:

        if room["number"] == number:
            room_type = room["type"]

    reservation_id = uuid.uuid4()

    message = send_booking_confirmation(
        login_name,
        check_in_date,
        check_out_date,
        room_type,
        total_cost,
        reservation_id,
        from_email,
    )

    smtp = smtplib.SMTP(HOST, PORT)

    status_code, response = smtp.ehlo()
    print(f"[*] Echoing the server: {status_code} {response}")

    status_code, response = smtp.starttls()
    print(f"[*] Starting TLS connection: {status_code} {response}")

    status_code, response = smtp.login(from_email, password)
    print(f"[*] Logging in: {status_code} {response}")

    smtp.sendmail(from_email, to_email, message)
    smtp.quit()


def open_client_list() -> list[dict[str]]:

    try:

        with open("guests.csv", "r") as file:

            reader = csv.DictReader(file)

            return [row for row in reader]

    except FileNotFoundError:

        return []


def is_valid_email(email: str) -> bool:

    if re.search(
        r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
        email,
        re.IGNORECASE,
    ):
        return True

    return False


def register(name: str, surname: str, email: str) -> list | None:

    guest_list = open_client_list()

    try:

        with open("guests.csv", "a", newline="") as guests:

            writer = csv.DictWriter(guests, fieldnames=["name", "surname", "email"])

            if len(guest_list) == 0:
                writer.writeheader()

            writer.writerow({"name": name, "surname": surname, "email": email})

    except FileNotFoundError:

        return []


def client_login(name: str, email: str) -> bool | list:

    try:

        with open("guests.csv", "r") as file:
            reader = csv.DictReader(file)

            for line in reader:
                if line["name"] == name and line["email"] == email:
                    return True

        return False

    except FileNotFoundError:
        print("File not found")
        return []


def open_available_rooms() -> list[dict[str]]:

    try:

        with open("available.csv", "r") as file:
            reader = csv.DictReader(file)

            rooms = [row for row in reader]

            return rooms

    except FileNotFoundError:
        print("File not found")
        return []


def open_unavailable_rooms():

    try:

        with open("unavailable.csv", "r") as file:

            reader = csv.DictReader(file)

            rooms = [line for line in reader]

            return rooms

    except FileNotFoundError:

        return []


def show_available_rooms(
    available: list[dict[str]], unavailable: list[dict[str]]
) -> list[dict[str]]:

    unavailable_room_number = [room["number"] for room in unavailable]

    return [room for room in available if room["number"] not in unavailable_room_number]


def room_price(available: list[dict[str]], room_number: str) -> int | None:
    for room in available:
        if room["number"] == room_number:
            return int(room["price"])


def stay_cost(nights: int, price_per_night: int) -> int:

    return nights * price_per_night


def book_room(room_num: str, check_in: str, check_out: str, name: str, email: str) -> None:

    available = open_available_rooms()

    unavailable = open_unavailable_rooms()

    for room in available:

        if room["number"] == room_num:

            room["check in"] = check_in
            room["check out"] = check_out
            room["name"] = name
            room["email"] = email

            unavailable.append(room)
            room_type = room["type"]

            with open("unavailable.csv", "w", newline="") as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=["number", "type", "price", "check in", "check out", "name", "email"],
                )
                writer.writeheader()

                for room in unavailable:
                    writer.writerow(room)

                print(f"Room {room_num}, a {room_type} room booked!")
                return

    print("Room not found")


def send_booking_confirmation(
    name,
    check_in,
    check_out,
    room_type,
    total_amount,
    reservation_number,
    from_email,
):

    return f"""Subject: Booking Confirmation - The Grand Ladora

            Dear {name},

            Thank you for choosing The Grand Ladora!

            We are delighted to confirm your booking with the following details:

                Reservation Number: GL-{reservation_number}
                Check-in Date: {check_in}
                Check-out Date: {check_out}
                Room Type: {room_type}
                Guest(s): {name}
                Total Amount: ZAR {total_amount:,.2f}

            We look forward to welcoming you. If you have any questions or need to make changes to your booking, feel free to contact us at {from_email} or 012 345 6789.

            Warm regards,
            The Grand Ladora Team"""


if __name__ == "__main__":
    main()
