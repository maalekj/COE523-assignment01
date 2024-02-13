import socket
from server_client_handler import run_client_handler

server_port = 12345


class Client:
    def __init__(self, client_socket, addr):
        self.client_socket = client_socket
        self.addr = addr
        self.client_handler_thread = run_client_handler(self)

    def send(self, message):
        self.client_socket.send(message)

    def receive(self):
        return self.client_socket.recv(1024)

    def close(self):
        self.client_socket.close()


def main():
    print("Welcoe to the server!")

    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", server_port))
    server_socket.listen(5)
    connected_clients = []

    print("Server is listening on port", server_port, ", waiting for a connection")
    while True:
        # Wait for a connection
        client_socket, addr = server_socket.accept()
        print("Got a connection from", addr, "Welcome!")
        connected_clients.append(Client(client_socket, addr))
        print("Connected clients:", connected_clients.__len__())


if __name__ == "__main__":
    main()
