import socket
import time
from server_client_handler import Client

server_port = 12345


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

        print("Got a connection from", addr, "start new thread!")
        new_client = Client(client_socket, addr)
        new_client.start()


if __name__ == "__main__":
    main()
