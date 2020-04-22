#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import ttk
from tkinter.ttk import Style


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
            msg_list.insert(tkinter.END, msg)
            # a bit of ***BAD CODE***, just to make the color different
            if "Enter your name" in msg or "enter group by sending the number" in msg or "what group do you want to go into" in msg:
                msg_list.itemconfig(msg_list.size() - 1, {'fg': 'green'})
            if "(created by" in msg:
                msg_list.itemconfig(msg_list.size() - 1, {'fg': 'SlateBlue4'})
            if "you have entered" in msg or "has joined the group" in msg:
                msg_list.itemconfig(msg_list.size() - 1, {'fg': 'royal blue'})
            if "you are currently in group" in msg or "Current online members:" in msg:
                msg_list.itemconfig(msg_list.size() - 1, {'fg': 'goldenrod4'})
            if "has left the group" in msg or "out of bounds! enter a valid" in msg:
                msg_list.itemconfig(msg_list.size() - 1, {'fg': 'red'})
            #below line is used to scroll through to end with each insert automatically
            msg_list.see(tkinter.END)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
s = ttk.Style()
s.theme_use("clam")
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
top.protocol("WM_DELETE_WINDOW", on_closing)

# ----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 3300
else:
    PORT = int(PORT)

BUFFER_SIZE = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution
