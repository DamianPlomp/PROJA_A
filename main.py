from datetime import *
import random

stations = ["Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag"]
#g
def get_information():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    station = random.choice(stations)
    message = input("You are at station " + station + ". Please tell us what you thought of your trip. (max 140 characters)\n")
    if len(message) > 140:
        print("That message was too long, please try again.")
        return get_information()
    anonymous = input("Would you like your review to be anonymous? Type Y for yes, and N for no.\n").lower()
    if anonymous == 'y':
        print("You will remain anonymous")
        name = "Anonymous"
    elif anonymous == 'n':
        name = input("Please tell us your name.\n")

    return message, dt_string, name, station

message, dt_string, name, station = get_information()

information = [name, dt_string, station, message]

with open('information.txt', 'a') as f:
    for info in information:
        f.write(info)
        f.write('\n')

