from datetime import *
import psycopg2
import random

stations = ["Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag"]

logged_in = False

def register_moderator():
    with open("moderators", "r+") as s:
        print("Here you can register to be a moderator so you can judge messages which people leave at their leave.\n")
        username = input("Please enter your name, which will be used as your username: ")
        accounts = s.readlines()
        for account in accounts:
            if username in account:
                print("That name is already registered, please enter the number 1, or your last name after your name.")
                return register_moderator()
        password = input("Please enter a password: ")
        email = input("Please enter an email: ")
        details = username + ";" + password + ":" + email
        s.write(details)
        s.write('\n')
    login_moderator()
def login_moderator(): # Details zijn vooraf al gemaakt (check txt file moderators)
    global logged_in
    start_menu = int(input("1. Login as moderator\n"
                             "2. Register to be a moderator\n"
                             "3. I want to submit a message\n>"))
    if start_menu == 1:
        username = input("username: ")
        password = input("password: ")
        details = username + ";" + password
        with open("moderators", "r+") as s:
            possible_accounts = s.readlines()
            for account in possible_accounts:
                stripped_string = account.split(':')[0]
                if details == stripped_string:
                    print("You are now logged in as a moderator")
                    logged_in = True
                    menu()
                else:
                    print("This user does not exist or you gave a wrong input")
                    return login_moderator()
    elif start_menu == 2:
        register_moderator()
    elif start_menu == 3:
        menu()
    else:
        print("Please give a valid option.")

def insert_information():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    station = random.choice(stations)
    message = input("You are at station " + station + ". Please tell us what you thought of your trip. (max 140 characters)\n>")
    if len(message) > 140:
        print("That message was too long, please try again.")
        return insert_information()
    anonymous = input("Would you like your review to be anonymous? Type Y for yes, and N for no.\n>").lower()
    if anonymous == 'y':
        print("You will remain anonymous")
        name = "Anonymous"
    elif anonymous == 'n':
        name = input("Please tell us your name.\n>")
    information = [message, dt_string, name, station, '\n']

    with open('information.txt', 'a') as s:
        for info in information:
            s.write(info)
            s.write('\n')

    return message, dt_string, name, station

def get_information():
    with open("moderators", "r+") as s:
        possible_accounts = s.readlines()
        for account in possible_accounts:
            email = account.split(':')[1]
    connection = psycopg2.connect(user="postgres", password="Plofkip17", host="localhost", database="StationsZuill", port="5432")
    c = connection.cursor()
    now = datetime.now()
    name_moderator = "Damian"
    dt_string = now.strftime("%d/%m/%Y")
    with open("information.txt", "r+") as s:
        lines = s.readlines()
        for i in range(0, len(lines), 6):
            print(f"There are {i} more messages ready to be judged.")
            line = lines[i]
            print(line)
            check_message = input("Is this message okay? (Y/N)\n>").lower()
            if check_message == 'y':
                print("You said this message was okay")
                good_or_bad = "good"
            elif check_message == 'n':
                good_or_bad = "bad"
            else:
                print("This was not a valid input.")
            insert_data = 'INSERT INTO processed_info(judgement, date, moderator_name, email) VALUES(%s,%s,%s,%s)'
            data = (good_or_bad, dt_string, name_moderator, email)
            c.execute(insert_data, data)
            connection.commit()
        c.close()
        connection.close()

def menu():
    while logged_in:
        moderator_menu_choices = int(input("1. get info\n"
                                           "2. logout\n>"))
        if moderator_menu_choices == 1:
            get_information()
        elif moderator_menu_choices == 2:
            break

    while not logged_in:
        default_menu_choices = int(input("1. insert info\n"
                                         "2. stop\n>"))
        if default_menu_choices == 1:
            insert_information()
        elif default_menu_choices == 2:
            break

login_moderator()


