import socket
import threading
from enum import Enum
import time

client_socket = None
client_id = None


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
        client_socket.send(message.encode())

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
        message = input("Enter a message to send to the server: ")
        # TODO: check if message is empty
        message_type = getMessageType(message)

        # if special message, delete first char '@'
        if message_type != MessageType.general_message:
            message = message[1:]
            # TODO: in case of quit, add the client id to the message

        # Send data to the server
        client_socket.send(message.encode())

        if message_type == MessageType.quit:
            print("Quitting")
            break
        # # Receive data from the server
        # data = client_socket.recv(1024)
        # print("Received from server:", data.decode())

    # # Close the socket
    # client_socket.close()


def receiveMasseges():
    global client_socket

    if client_socket is None:
        print("Client socket is None, exiting")
        return

    while True:
        # Receive data from the server
        data = client_socket.recv(1024)
        print("\nReceived from server:", data.decode())

    # Close the socket
    client_socket.close()


if __name__ == "__main__":
    print("Welcome to the chat app")

    client_id = input("What would you like others to call you?")

    # Connect to the server
    while True:
        connected = connectToServer()
        if connected:
            break

    message_listner = threading.Thread(
        target=receiveMasseges
    )  # a thread to handle receiving messages from the server

    message_listner.start()  # start the thread

    sendUserMasseges()  # Run the main function
