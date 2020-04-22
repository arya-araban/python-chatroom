#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from usefulMethods import change_inside_tuple_value

clients = {}
addresses = {}

HOST = ''
group_list = []
PORT = 3300
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)
previous_message_list = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
entered_group_temp = -1


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print(f"{client_address[0]}:{client_address[1]} has connected.")
        client.send(bytes("Enter your name", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client_group, args=(client,)).start()


def handle_client_group(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    entered_group = -1
    name = client.recv(BUFFER_SIZE).decode("utf8")
    welcome = f'Welcome {name}! enter group by sending the number, or create your own new group by sending the name'
    client.send(bytes(welcome, "utf8"))
    # remember that group_list has a structure of (group_name, group_creator_name)
    for index, group in enumerate(group_list):
        grp = f"{str(index)}: {group[0]} (created by {group[1]})"
        print(index)
        time.sleep(0.005)
        client.send(bytes(grp, "utf8"))
    while entered_group == -1:
        create_group_or_group_index = client.recv(BUFFER_SIZE).decode("utf8")
        if create_group_or_group_index.isdigit():
            entered_group = int(create_group_or_group_index)
            try:
                join_msg = f"you have entered {group_list[int(create_group_or_group_index)][0]}! (group {create_group_or_group_index})"
            except IndexError:
                join_msg = f"out of bounds! enter a valid group number"
                entered_group = -1
            client.send(bytes(join_msg, "utf8"))
        else:
            group_list.append((create_group_or_group_index, name))
            grp = f"{str(len(group_list) - 1)}: {group_list[-1][0]} (created by {name})"
            client.send(bytes(grp, "utf8"))
        # add the new person to the clients dictionary
    clients[client] = name, entered_group
    broadcast(bytes(f"{name} has joined the group!", "utf8"), entered_group, exception_socket=client)

    for message in previous_message_list:
        # searching for previous messages in specific group
        # remember: previous_message_list has structure of ('message_sender_name', b'the message itself', group_index)
        if message[2] == entered_group:
            msg = message[0] + ": " + str(message[1], 'utf8')
            time.sleep(0.005)
            client.send(bytes(msg, "utf8"))

    while True:
        msg = client.recv(BUFFER_SIZE)
        # client wants to quit

        if msg == bytes("{quit}", "utf8"):
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes(f"{name} has quit the chat.", "utf8"), entered_group)
            break

        elif msg == bytes("{members}", "utf8"):
            online_members_group = 'Current online members: '
            for sock in clients:
                if clients[sock][1] == entered_group:
                    online_members_group = online_members_group + clients[sock][0] + ' || '
            client.send(bytes(online_members_group, 'utf8'))

        elif msg == bytes("{whereAmI}", "utf8"):
            client.send(
                bytes(f'you are currently in group {group_list[entered_group][0]} (group {entered_group})', 'utf8'))

        elif msg == bytes("{exitGP}", "utf8"):
            broadcast(bytes(f"{name} has left the group.", "utf8"), entered_group)
            entered_group = -1
            # here we are making it so that the left user isn't in reality in any group
            clients[client] = change_inside_tuple_value(clients[client], 1, -1)
            # like used above, we need a very small sleep so that the lines don't overlap
            time.sleep(0.005)
            new_grp_msg = f'what group do you want to go into, {name}?'
            client.send(bytes(new_grp_msg, "utf8"))
            for index, group in enumerate(group_list):
                grp = f"{str(index)}: {group[0]} (created by {group[1]})"
                print(index)
                time.sleep(0.005)
                client.send(bytes(grp, "utf8"))
            while entered_group == -1:
                gp_index = client.recv(BUFFER_SIZE).decode("utf8")
                if gp_index.isdigit():
                    entered_group = int(gp_index)
                    try:
                        join_msg = f"you have entered {group_list[int(gp_index)][0]}! (group {gp_index})"
                    except IndexError:
                        join_msg = f"out of bounds! enter a valid group number"
                        entered_group = -1
                    client.send(bytes(join_msg, "utf8"))
                    if entered_group != -1:
                        clients[client] = change_inside_tuple_value(clients[client], 1, entered_group)
                        for message in previous_message_list:
                            if message[2] == entered_group:
                                msg = message[0] + ": " + str(message[1], 'utf8')
                                time.sleep(0.005)
                                client.send(bytes(msg, "utf8"))
                        broadcast(bytes(f"{name} has joined the group!", "utf8"), entered_group,
                                  exception_socket=client)
                        continue

        # client sends normal message
        else:
            broadcast(msg, entered_group, prefix=name + ": ")
            # a list of tuple for previous messages
            previous_message_list.append((name, msg, entered_group))
            print(previous_message_list[-1])


def broadcast(msg, group_number, exception_socket=None, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        if clients[sock][1] == group_number and sock != exception_socket:
            sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    # the QUEUE we have can handle 5 at a time
    SERVER.listen(5)
    print("Waiting for connection...")
    # a thread that has the accept_incoming_connections as its target
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    # start running the thread...
    ACCEPT_THREAD.start()
    # with .join() we wait until the ACCEPT_THREAD is finished executing
    ACCEPT_THREAD.join()
    SERVER.close()
