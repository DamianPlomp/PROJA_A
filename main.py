from datetime import *
import psycopg2
import random

stations = ["Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag"]

logged_in = False
logged_in_user = None

def register_moderator():
    connection = psycopg2.connect(user="postgres", password="Plofkip17", host="localhost", database="StationsZuill", port="5432")
    c = connection.cursor()
    username = input("username: ")
    email = input("email: ")
    password = input("password: ")
    registered_moderators = ('SELECT * FROM moderators')
    c.execute(registered_moderators)
    if username in registered_moderators:
        print("This username has already been taken, please choose a different one.")
        logged_in_user = username
        return register_moderator()
    else:
        details = (username, email, password)
        insertion = ('INSERT INTO moderators (username, email, password) VALUES (%s,%s,%s)')
        c.execute(insertion, details)

    connection.commit()
    c.close()

def login_moderator(): # Details zijn vooraf al gemaakt (check txt file moderators)
    global logged_in
    global logged_in_user
    connection = psycopg2.connect(user="postgres", password="Plofkip17", host="localhost", database="StationsZuill", port="5432")
    c = connection.cursor()

    start_menu = int(input("1. Login as moderator\n"
                             "2. Register to be a moderator\n"
                             "3. I want to submit a message\n>"))
    if start_menu == 1:
        username = input("username: ")
        password = input("password: ")
        c.execute('SELECT username, password FROM moderators')
        fetched = c.fetchall()
        for moderator in fetched:
            if username and password in moderator:
                print("You are now logged in as a moderator.")
                logged_in = True
                logged_in_user = username
                menu()
            else:
                print("This user does not exist in our database.")
                return login_moderator()
    elif start_menu == 2:
        register_moderator()
    elif start_menu == 3:
        menu()
    else:
        print("Please give a valid option.")

    connection.commit()
    c.close()

def insert_message():
    now = datetime.now()
    submissionTimeStamp = now.strftime("%d/%m/%Y %H:%M:%S")
    station = random.choice(stations)
    message = input("You are at station " + station + ". Please tell us what you thought of your trip. (max 140 characters)\n>")
    if len(message) > 140:
        print("That message was too long, please try again.")
        return insert_message()
    anonymous = input("Would you like your review to be anonymous? Type Y for yes, and N for no.\n>").lower()
    if anonymous == 'y':
        print("You will remain anonymous")
        name = "Anonymous"
    elif anonymous == 'n':
        name = input("Please tell us your name.\n>")
    information = [message, submissionTimeStamp, name, station, '\n']

    with open('information.txt', 'a') as s:
        for info in information:
            s.write(info)
            s.write('\n')

    return message, submissionTimeStamp, name, station

def push_checked_message():
    connection = psycopg2.connect(user="postgres", password="Plofkip17", host="localhost", database="StationsZuill", port="5432")
    c = connection.cursor()
    c.execute("SELECT email FROM moderators WHERE username = %s", [logged_in_user])
    email = c.fetchall()
    now = datetime.now()
    checkTimeStamp = now.strftime("%d/%m/%Y %H:%M:%S")
    with open("information.txt", "r+") as s:
        lines = s.readlines()
        for i in range(0, len(lines), 9):
            line = lines[i]
            station = line
        for i in range(0, len(lines), 8):
            line = lines[i]
            name = line
        for i in range(0, len(lines), 7):
            line = lines[i]
            submissionTimeStamp = line
        for i in range(0, len(lines), 6):
            line = lines[i]
            print(line)
            message = line
            check_message = input("Is this message okay? (Y/N)\n>").lower()
            if check_message == 'y':
                print("You said this message was okay")
                show = True
            elif check_message == 'n':
                show = False
            else:
                print("This was not a valid input.")

            insertion = ('INSERT INTO bericht (message, submissionTimestamp, name, station, username, email, checkTimestamp, show) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)')
            insertion_data = (message, submissionTimeStamp, name, station, logged_in_user, email, checkTimeStamp, show)
            c.execute(insertion, insertion_data)
        s.truncate(0)
    connection.commit()
    c.close()

def menu():
    global logged_in_user
    while logged_in:
        moderator_menu_choices = int(input("1. check messages\n"
                                           "2. logout\n>"))
        if moderator_menu_choices == 1:
            push_checked_message()
        elif moderator_menu_choices == 2:
            logged_in_user = None
            break

    while not logged_in:
        default_menu_choices = int(input("1. insert info\n"
                                         "2. stop\n>"))
        if default_menu_choices == 1:
            insert_message()
        elif default_menu_choices == 2:
            break

login_moderator()