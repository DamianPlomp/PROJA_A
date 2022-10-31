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

    facilities_there = []

    query = ("SELECT * FROM station_service WHERE station_city = %s")
    c.execute(query, (station,))
    booleans = c.fetchall()
    for facility, facility_true in zip(facilities, booleans[0]):
        if isinstance(facility_true, str):
            facilities_there.append(facility_true)
        elif facility_true:
            facilities_there.append(facility)

    connection.commit()
    c.close()

    return facilities_there

def get_messages():
    connection = psycopg2.connect(user="postgres", password="Plofkip17", host="localhost", database="StationsZuill",
                                  port="5432")
    c = connection.cursor()

    messageslst = []

    c.execute('SELECT TOP 5 message, submissionTimeStamp FROM bericht ORDER BY id DESC')
    message_info = c.fetchall()
    for msg in message_info:
        messageslst.append(msg)

    connection.commit()
    c.close()

    return messageslst


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

    facilities = Label(sw, text=is_facility(station), pady=10)
    facilities.grid(row=5, column=0, columnspan=4, pady=20)

    messages = Label(sw, text=get_messages(), borderwidth=1, relief='groove')
    messages.grid(row=1, column=1, pady=20)

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

    return station


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

main_window()