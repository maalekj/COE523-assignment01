import socket
from server_client_handler import run_client_handler

server_port = 12345


class Client:
    def __init__(self, client_socket, addr, client_id):
        self.client_socket = client_socket
        self.addr = addr
        self.client_id = client_id
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

        # Receive client Connect message with client id
        message = client_socket.recv(1024).decode()
        if (
            message[:8] != "Connect " or len(message) < 8
        ):  # Check if the message is a Connect message
            continue  # if a message is not a Connect message, ignore the client
        else:
            client_id = message[8:]

        print("Got a connection from", addr, "Welcome ", client_id, "!")
        connected_clients.append(Client(client_socket, addr, client_id))
        print("Connected clients:", connected_clients.__len__())


if __name__ == "__main__":
    main()
