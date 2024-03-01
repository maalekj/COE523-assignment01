import socket
import time
import threading
from server_client_handler import Client, check_clients_alive, num_of_connected_clients

server_port = 12345
AllowedClientsNumber = 32


def main():
    print("Welcoe to the server!")

    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # start keep alive checker thread
    keep_alive_checker_thread = threading.Thread(target=check_clients_alive)
    keep_alive_checker_thread.start()

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

        if num_of_connected_clients() + 1 > AllowedClientsNumber:
            print("Too many connected clients, can't accept new connection")
            client_socket.close()
            continue

        print("Got a connection from", addr, "start new thread!")
        new_client = Client(client_socket, addr)
        new_client.start()


if __name__ == "__main__":
    main()
