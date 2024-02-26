import threading

# shared data with all clients handlers
connected_clients = {}


class Client(threading.Thread):
    def __init__(self, client_socket, addr):
        self.client_socket = client_socket
        self.addr = addr
        self.client_id = None
        # self.client_id = client_id
        # self.client_handler_thread = run_client_handler(self)
        threading.Thread.__init__(self)

    def run(self):
        while True:
            message = self.client_socket.recv(1024).decode()
            print("Received from client:", message)
            self.handle_message(str(message))

    def send(self, message):
        self.client_socket.send(message.encode())

    def receive(self):
        return self.client_socket.recv(1024)

    def close(self):
        self.client_socket.close()

    def handle_message(self, message):
        # Perform actions based on message content
        if message[:8] == "Connect " and len(message) >= 8:
            if self.client_id is not None:
                print("Client id already set")
                self.send("Client id already set")
                return
            self.client_id = message[8:]
            connected_clients[self.client_id] = self

        elif message == "action2":
            # Perform action 2
            pass
        else:
            print("Unknown message:", message)
            # Handle unknown message
            pass
