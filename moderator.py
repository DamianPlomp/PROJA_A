from datetime import *
import psycopg2

logged_in_user = 'Damian'
logged_in = False
#logged_in_user = None

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
                             "2. Register to be a moderator\n"))
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
    else:
        print("Please give a valid option.")

    connection.commit()
    c.close()

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

login_moderator()

