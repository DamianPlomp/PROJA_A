from datetime import *
import psycopg2
import random
import tkinter
from tkinter import *
from PIL import ImageTk, Image

stations = ["Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag"]

logged_in = False
logged_in_user = None
buttonIsClicked = False
station = None

def is_facility(station):
    facilities = ['station_city', 'country', 'ov_bike', 'elevator', 'toilet', 'park_and_ride']

    connection = psycopg2.connect(user="postgres", password="Plofkip17", host="localhost", database="StationsZuill",
                                  port="5432")
    c = connection.cursor()

    query = ("SELECT * FROM station_service WHERE station_city = %s")
    c.execute(query, station)
    booleans = c.fetchall()
    for facility, facility_true in zip(facilities, booleans[0]):
        if facility_true:
            print(facility)

    connection.commit()
    c.close()

def station_window(station):
    sw = tkinter.Toplevel()

    sw.geometry("1024x538")

    image = Image.open("s_background.png")
    bg = ImageTk.PhotoImage(image)
    my_label = Label(sw, image=bg)
    my_label.place(x=0, y=0)

    message = Label(sw, text='Laat hier je bericht achter over wat je van de reiservaring vond:')
    message.grid(row=0, column=0)

    message_text = Text(sw, width=40, height=10, pady=10, padx=10)
    message_text.grid(row=1, column=0, pady=20)

    naam_info = Label(sw, text='Laat hier je naam achter, als je anoniem wilt blijven vul dan "anoniem" in.')
    naam_info.grid(row=2, column=0)

    name_text = Text(sw, width=40, height=2, pady=10, padx=10)
    name_text.grid(row=3, column=0, pady=20)

    submit_button = tkinter.Button(sw, text='Submit', command=lambda: insert_message(message_text, name_text, station))
    submit_button.grid(row=4, column=0, pady=20)

    facilities = Label(sw, text=is_facility(station))
    facilities.grid(row=5, column=0, columnspan=1, pady=20)

    return message_text, name_text, station

def main_window():
    window = Tk()
    window.geometry("1024x538")

    image = Image.open("s_background.png")
    bg = ImageTk.PhotoImage(image)

    my_label = Label(window, image=bg)
    my_label.place(x=0, y=0)

    button1 = tkinter.Button(window, text='Dordrecht', width=40, height=10, command=lambda: station_window('Dordrecht'))
    button1.grid(row=0, column=0, padx=25, pady=10)

    button2 = tkinter.Button(window, text='Delft', width=40, height=10, command=lambda: station_window('Delft'))
    button2.grid(row=0, column=1, padx=25, pady=10)

    button3 = tkinter.Button(window, text='Deventer', width=40, height=10, command=lambda: station_window('Deventer'))
    button3.grid(row=0, column=2, padx=25, pady=10)

    button4 = tkinter.Button(window, text='Enschede', width=40, height=10, command=lambda: station_window('Enschede'))
    button4.grid(row=1, column=0, padx=25, pady=10)

    button5 = tkinter.Button(window, text='Gouda', width=40, height=10, command=lambda: station_window('Gouda'))
    button5.grid(row=1, column=1, padx=25, pady=10)

    button6 = tkinter.Button(window, text='Groningen', width=40, height=10, command=lambda: station_window('Groningen'))
    button6.grid(row=1, column=2, padx=25, pady=10)

    button7 = tkinter.Button(window, text='Den Haag', width=40, height=10, command=lambda: station_window('Den Haag'))
    button7.grid(row=3, column=1, padx=25, pady=10)

    exit_button = tkinter.Button(window, text='Exit', width=40, height=10, command=window.destroy)
    exit_button.grid(row=3, column=2, padx=25, pady=10)

    window.mainloop()

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

def insert_message(message_text, name_text, station):
    now = datetime.now()
    submissionTimeStamp = now.strftime("%d/%m/%Y %H:%M:%S")
    station = station
    message = message_text.get(1.0, "end-1c")
    name = name_text.get(1.0, "end-1c")
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

main_window()