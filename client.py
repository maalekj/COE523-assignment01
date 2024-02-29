import pickle
import socket
import threading
from enum import Enum
import time

client_socket = None
client_id = None
stop_thread = False
KEEP_ALIVE_PERIOD = 0


class MessageType(Enum):
    quit = 1
    connect = 2
    list = 3
    general_message = 4


def getMessageType(message):
    if message == "@Quit":
        return MessageType.quit
    elif message == "@List":
        return MessageType.list
    else:
        return MessageType.general_message


# create a socket object and connect to the server
def connectToServer():
    global client_socket, client_id

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = input("Enter the server ip: ")
    server_port = input("Enter the server port: ")

    # Define the server address and port
    try:
        server_address = (server_ip, int(server_port))
        # Connect to the server
        client_socket.connect(server_address)
        print("Connected to server at", server_address)

        # Send the client id to the server
        message = "Connect " + client_id
        client_socket.send(pickle.dumps(message))

    except ValueError:
        print("Invalid port number")
        return False
    except ConnectionRefusedError:
        time.sleep(1)
        print("couldn't connect to server. Check ip and port")
        return False

    return True


# get user input and do action or send massege to the server
def sendUserMasseges():
    global client_socket

    if client_socket is None:
        print("Client socket is None, exiting")
        return

    while True:
        # Prompt the user for input
        message = input()
        # check if message is empty
        if message == "":
            continue

        message_type = getMessageType(message)

        # if special message, delete first char '@'
        if message_type != MessageType.general_message:
            # remove the @ char
            message = message[1:]

            if message_type == MessageType.quit:
                message = message + " " + client_id

        # Send data to the server
        client_socket.send(pickle.dumps(message))

        if message_type == MessageType.quit:
            print("Quitting")
            break


def receiveMasseges():
    global client_socket, KEEP_ALIVE_PERIOD, stop_thread

    if client_socket is None:
        print("Client socket is None, exiting")
        return

    while not stop_thread:
        try:
            # Receive data from the server
            data = client_socket.recv(1024)
            data = pickle.loads(data)

            if data == "":
                print("server connection is closed, exiting")
                client_socket.close()
                return
            elif data[:14] == "Clients##List ":
                data = data[14:]
                print("available clients:", data)
                continue
            elif data[:11] == "KEEPALIVE##":
                period_in_seconds = int(data[11:])

                if period_in_seconds > 1:
                    # in case the server wants the client to send keep alive every 2 seconds or more then the client should send keep alive every period - 1 seconds to be in safe side
                    KEEP_ALIVE_PERIOD = period_in_seconds - 1
                else:
                    # in case the server wants the client to send keep alive every second or less then the client should send keep alive every 0.5 seconds
                    KEEP_ALIVE_PERIOD = period_in_seconds / 2

                print("KEEP_ALIVE_PERIOD:", KEEP_ALIVE_PERIOD)
                continue

            print("\n", data)
        except ConnectionResetError and EOFError:
            print("server connection is closed, exiting")
            client_socket.close()
            return


def sendKeepAlive():
    global client_socket, KEEP_ALIVE_PERIOD, stop_thread
    while not stop_thread:
        if client_socket is not None and KEEP_ALIVE_PERIOD > 0:
            client_socket.send(pickle.dumps("Alive"))
            print("sent keep alive")
            time.sleep(KEEP_ALIVE_PERIOD)

    print("keep alive thread is done")


if __name__ == "__main__":
    print("Welcome to the chat app")

    client_id = input("What would you like others to call you?")

    # Connect to the server
    while True:
        connected = connectToServer()
        if connected:
            break

    # a thread to handle receiving messages from the server
    message_listner = threading.Thread(target=receiveMasseges)
    message_listner.start()  # start the thread

    # a thread to send keep alive to the server
    keepAlive_sender = threading.Thread(target=sendKeepAlive)
    keepAlive_sender.start()  # start the thread

    sendUserMasseges()  # Run the main function that get user input and send it to the server

    # if sendUserMasseges() is done, close the receiveMasseges thread
    stop_thread = True
    message_listner.join()
