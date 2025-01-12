import csv
import sys
import calendar
from datetime  import date
from prettytable import PrettyTable

table = PrettyTable(["Room Number", "Room Type", "Price"])

def main():


    print("Welcome to the Grand Ladora \nPlease register before making a booking")

    print()

    while True:


        print("1.Register \n2. Login")

        entry = input("Choose an option: ")

        if entry == "1" or entry == "Register":

            name = input("Please enter your name: ")

            surname = input("Please enter your surname: ")

            email = input("Please enter your email adddress: ")

            register(name, surname, email)

            print(f"Guest {name} {surname} successfully registered\nProceed to login now")


        elif entry == "2" or entry == "Login":
            login_name = input("Enter your name: ")

            login_email = input("Enter your email: ")

            if client_login(login_name, login_email):
                print("Login successful!")
                break
            else:
                print("Login failed! \nPlease check your details or register")

        else:
            print("Invalid selection")    

    current_date = date.today()

    current_date = str(current_date)

    year, month, day = current_date.split("-")

    while True:

        try:

            print(calendar.month(int(year), int(month)))

            check_in = int(input("Please choose a check-in date: "))
            break

        except ValueError:

            print("Not a valid date, try again.")


    while True:

        try:


            print(calendar.month(int(year), int(month)))

            check_out = int(input("Please choose a check-out date: "))
            break

        except ValueError:

            print(f"{check_out} is not a valid date")


    available = open_available_rooms()

    unavailable = open_unavailable_rooms()

    print("These are the available rooms to book")

    available_rooms_display = show_available_rooms(available, unavailable)

    for room in available_rooms_display:
        table.add_row([room['number'], room['type'], room['price']])

    print(table)

    number = input("Pick a room number: ")

    price = room_price(available, number)


    check_in_date = year + "-" + month + "-" + str(check_in)
    check_out_date = year + "-" + month + "-" + str(check_out)
    

    nights_spent = check_out - check_in

    total_cost = stay_cost(nights_spent, price)

    print(f"Your stay for {nights_spent} night(s) is ZAR {total_cost:,.2f}")

    book_room(number, check_in_date, check_out_date)

def open_client_list() -> (list[dict[str]]):

    try:

        with open("guests.csv", "r") as file:

            reader = csv.DictReader(file)

            return [row for row in reader]


    except FileNotFoundError:

        return []


def register(name: str, surname: str, email: str) -> (list | None):

    guest_list = open_client_list()

    try:

        with open("guests.csv", "a", newline="") as guests:

            writer = csv.DictWriter(guests, fieldnames=["name", "surname", "email"])

            if len(guest_list) == 0:
                writer.writeheader()

            writer.writerow({"name":name, "surname": surname, "email" : email})

    except FileNotFoundError:

        return []

def client_login(name: str, email: str) -> (bool | list) :
    

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

def open_available_rooms()  -> (list[dict[str]]):

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

def show_available_rooms(available: list[dict[str]], unavailable: list[dict[str]]) -> list[dict[str]]:

    unavailable_room_number = [room["number"] for room in unavailable]

    return [room for room in available if room["number"] not in unavailable_room_number]

def room_price(available: list[dict[str]], room_number: str) -> (int | None):
    for room in available:
        if room["number"] == room_number:
            return int(room['price'])

def stay_cost(nights: int, price_per_night: int) -> int:

    return nights * price_per_night

def book_room(room_num: str, check_in: str, check_out: str) -> None:

    available = open_available_rooms()

    unavailable = open_unavailable_rooms()


    for room in available:

        if room["number"] == room_num:

            room["check in"] = check_in
            room["check out"] = check_out

            unavailable.append(room)
            room_type = room["type"]
            

            with open("unavailable.csv", "w", newline="") as file:

                writer = csv.DictWriter(file, fieldnames=["number", "type", "price", "check in", "check out"])
                writer.writeheader()

                # writer.writerows(unavailable)

                for room in unavailable:
                    writer.writerow(room)


                print(f"Room {room_num}, a {room_type} room booked!")
                return

    print("Room not found")

if __name__ == "__main__":
    main()