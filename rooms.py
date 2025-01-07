import csv
import calendar
from datetime  import date
from prettytable import PrettyTable

table = PrettyTable(["Room Number", "Room Type", "Price"])

def main():

    while True:


        guest = {}

        name = input("Please enter your name ")

        surname = input("Please enter your surname ")

        email = input("Please enter your email adddress ")

        guest["name"] = name

        guest["surname"] = surname

        guest["email"] = email

        

        clients = [guest]

        register(clients)

        print("Please login to book a room with us")

        login_name = input("Enter your name ")

        login_email = input("Enter your email ")

        if client_login(clients, login_name, login_email):
            print("Login successful")
            while not client_login(clients, login_name, login_email):
                print("Details do not exist, try again.")
            break

        



    available = open_available_rooms()

    unavailable = open_unavailable_rooms()

    print("These are the available rooms to book")

    available_rooms_display = show_available_rooms(available, unavailable)

    for room in available_rooms_display:
        table.add_row([room['number'], room['type'], room['price']])

    print(table)

    current_date = date.today()

    current_date = str(current_date)

    year, month, day = current_date.split("-")


    number = input("Pick a room number: ")

    price = room_price(available, number)

    print(calendar.month(int(year), int(month)))

    try:


        check_in = int(input("Please choose a check-in date: "))

    except ValueError:

        print("Not a valid date")


    print(calendar.month(int(year), int(month)))

    check_out = int(input("Please choose a check-out date: "))

    check_in_date = year + "-" + month + "-" + str(check_in)
    check_out_date = year + "-" + month + "-" + str(check_out)
    

    nights_spent = check_out - check_in

    total_cost = stay_cost(nights_spent, price)

    print(f"Your stay for {nights_spent} night(s) is ZAR {total_cost:,.2f}")

    book_room(number, check_in_date, check_out_date)

def register(guest_list):

    with open("guests.csv", "w", newline="") as guests:

        writer = csv.DictWriter(guests, fieldnames=["name", "surname", "email"])
        writer.writeheader()

        writer.writerows(guest_list)

def client_login(guest_list, name, email):
    

    for item in guest_list:
        print(item)

        if item["name"] == name and item["email"] == email:
            return True
       
    return False



def open_available_rooms():

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

def show_available_rooms(available, unavailable):

    unavailable_room_number = [room["number"] for room in unavailable]

    return [room for room in available if room["number"] not in unavailable_room_number]

def room_price(available, room_number):
    for room in available:
        if room["number"] == room_number:
            return int(room['price'])

def stay_cost(nights, price_per_night):

    return nights * price_per_night

def book_room(room_num, check_in, check_out):

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