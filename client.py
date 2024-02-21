import socket
import threading

client_socket = None


# create a socket object and connect to the server
def connectToServer():
    global client_socket

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
    except ValueError:
        print("Invalid port number")
        return False
    except ConnectionRefusedError:
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

        # Send data to the server
        client_socket.send(message.encode())

        # # Receive data from the server
        # data = client_socket.recv(1024)
        # print("Received from server:", data.decode())

    # # Close the socket
    # client_socket.close()


if __name__ == "__main__":
    print("Welcome to the chat app")

    # Connect to the server
    while True:
        connected = connectToServer()
        if connected:
            break

    # TODO: Create a thread to handle receiving messages from the server
    sendUserMasseges()  # Run the main function
