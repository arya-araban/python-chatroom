# NO GROUP SERVER AND CLIENT

# SERVER
'''#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = ''
group_list = []
PORT = 33000
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)
previous_message_list = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print(f"{client_address[0]}:{client_address[1]} has connected.")
        client.send(bytes("Enter your name", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

#
# def add_to_previous_messages():
#     while True:
#

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFFER_SIZE).decode("utf8")
    welcome = f'Welcome {name}! type {quit} if you want to exit.'
    client.send(bytes(welcome, "utf8"))
    for message in previous_message_list:
        msg = message[0]+": "+str(message[1], 'utf8')
        time.sleep(0.001)
        client.send(bytes(msg, "utf8"))
    msg = f"{name} has joined the chat!"
    #tells the other clients that this person has joined
    broadcast(bytes(msg, "utf8"))
    #add the new person to the clients dictionary
    clients[client] = name

    while True:
        msg = client.recv(BUFFER_SIZE)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
            #a list of tuple for previous messages
            previous_message_list.append((name, msg))
            print (previous_message_list[-1])
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes(f"{name} has left the chat.", "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    #the QUEUE we have can handle 5 at a time
    SERVER.listen(5)
    print("Waiting for connection...")
    #a thread that has the accept_incoming_connections as its target
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    #start running the thread...
    ACCEPT_THREAD.start()
    #with .join() we wait until the ACCEPT_THREAD is finished executing
    ACCEPT_THREAD.join()
    SERVER.close()
'''

# CLIENT
'''#!/usr/bin/env python3
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
    PORT = 33000
else:
    PORT = int(PORT)


BUFFER_SIZE = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution'''

# exitGP
'''new_grp_msg = f'what group do you want to go into, {name}?'
            client.send(bytes(new_grp_msg, "utf8"))
            for index, group in enumerate(group_list):
                grp = f"{str(index)}: {group}"
                print(index)
                time.sleep(0.001)
                client.send(bytes(grp, "utf8"))
            while entered_group == -1:
                gp_index = client.recv(BUFFER_SIZE).decode("utf8")
                if gp_index.isdigit():
                    entered_group = int(gp_index)
                    join_msg = f"you have entered {group_list[int(gp_index)]}! (group {gp_index})"
                    client.send(bytes(join_msg, "utf8"))'''

# old handle_client_message
'''# def handle_client_message(client):  # Takes client socket as argument.
#     """Handles a single client connection."""
#     if entered_group_temp != -1:
#         name = client.recv(BUFFER_SIZE).decode("utf8")
#         welcome = f'Welcome {name}! type {quit} if you want to exit.'
#         client.send(bytes(welcome, "utf8"))
#         for message in previous_message_list:
#             msg = message[0] + ": " + str(message[1], 'utf8')
#             time.sleep(0.001)
#             client.send(bytes(msg, "utf8"))
#         msg = f"{name} has joined the chat!"
#         # tells the other clients that this person has joined
#         broadcast(bytes(msg, "utf8"))
#         # add the new person to the clients dictionary
#         clients[client] = name
#
#     while True and entered_group_temp != -1:
#         msg = client.recv(BUFFER_SIZE)
#         if msg != bytes("{quit}", "utf8"):
#             broadcast(msg, name + ": ")
#             # a list of tuple for previous messages
#             previous_message_list.append((name, msg, entered_group_temp))
#             print(previous_message_list[-1])
#         else:
#             client.send(bytes("{quit}", "utf8"))
#             client.close()
#             del clients[client]
#             broadcast(bytes(f"{name} has left the chat.", "utf8"))
#             break'''
