import socket
import time
from server_client_handler import Client

server_port = 12345
connected_clients = {}


def main():
    print("Welcoe to the server!")

    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            server_socket.bind(("localhost", server_port))
            break
        except OSError:
            print("Port", server_port, "is already in use, try again later")
            time.sleep(10)

    server_socket.listen(5)

    print("Server is listening on port", server_port, ", waiting for a connection")
    while True:
        # Wait for a connection
        client_socket, addr = server_socket.accept()

        # # Receive client Connect message with client id
        # message = client_socket.recv(1024).decode()
        # if (
        #     message[:8] != "Connect " or len(message) < 8
        # ):  # Check if the message is a Connect message
        #     continue  # if a message is not a Connect message, ignore the client
        # else:
        #     client_id = message[8:]

        print("Got a connection from", addr, "start new thread!")
        new_client = Client(client_socket, addr)
        new_client.start()

        print("Connected clients:", connected_clients.__len__())


if __name__ == "__main__":
    main()
