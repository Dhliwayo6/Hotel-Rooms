import csv



def main():

    available = open_available_rooms()

    print(available)

    unavailable = open_unavailable_rooms()

    print(unavailable)

    print("These are the available rooms to book")

    available_rooms_display = show_available_rooms(available, unavailable)

    for room in available_rooms_display:
        print(f"Room number {room['number']} -> {room['type']}")

    number = input("Pick a room number: ")

    book_room(number)


def open_available_rooms():

    with open("available.csv", "r") as file:
        reader = csv.DictReader(file)

        rooms = [row for row in reader]

        return rooms


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

    print(unavailable_room_number)

    available_room_number = [room for room in available if room["number"] not in unavailable_room_number]

    print(available_room_number)

    return(available_room_number)


def book_room(room_num):

    available = open_available_rooms()

    unavailable = open_unavailable_rooms()


    for room in available:

        if room["number"] == room_num:

            unavailable.append(room)

            with open("unavailable.csv", "w") as file:

                writer = csv.DictWriter(file, fieldnames=["number", "type"])
                writer.writeheader()

                # writer.writerows(unavailable)

                for room in unavailable:
                    writer.writerow(room)


                print(f"Room {room_num} booked!")
                print(unavailable)
                return

    print("Room not found")

if __name__ == "__main__":
    main()
