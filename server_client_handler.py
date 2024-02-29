import pickle
import threading
import time

# shared data with all clients handlers
connected_clients = {}
clinets_keep_alive_period_in_seconds = 10


class Client(threading.Thread):
    def __init__(self, client_socket, addr):
        self.client_socket = client_socket
        self.addr = addr
        self.client_id = None
        self.last_keep_alive = time.time()
        # self.client_id = client_id
        # self.client_handler_thread = run_client_handler(self)
        threading.Thread.__init__(self)

    def run(self):
        while True:
            message = ""
            try:
                message = self.client_socket.recv(1024)
                message = pickle.loads(message)
            except ConnectionResetError and OSError:
                pass
            if message == "":
                print("Client socket is None, exiting")
                self.close()
                time.sleep(1)
                return

            self.handle_message(str(message))

    def send(self, message):
        self.client_socket.send(pickle.dumps(message))

    def receive(self):
        return self.client_socket.recv(1024)

    def close(self):
        self.client_socket.close()

    def handle_message(self, message):
        # Perform actions based on message content
        if message[:8] == "Connect " and len(message) >= 8:
            if self.client_id is not None:
                exception = "Client id already set"
                print(exception)
                self.send(exception)
                return
            self.client_id = message[8:]
            connected_clients[self.client_id] = self

            # notify the client that it is connected and the keep alive period that the client should send whithin to be considered alive
            self.send("KEEPALIVE##" + str(clinets_keep_alive_period_in_seconds))

        elif message == "Quit " + self.client_id:
            print("client", self.client_id, "is quitting")
            # remove the client from the connected_clients dictionary
            if self.client_id in connected_clients:
                del connected_clients[self.client_id]

            self.close()
            # Perform action 2
            pass

        elif message == "List":
            self.send("Clients##List " + str(list(connected_clients.keys())))

        elif message == "Alive":
            print("client", self.client_id, "is alive")
            # Perform action 3
            pass

        elif " " in message:
            receiver_id, message = message.split(" ", 1)
            if receiver_id in connected_clients:
                connected_clients[receiver_id].send(self.client_id + ":" + message)
            else:
                self.send("server: Client " + receiver_id + " is not connected")

        else:
            self.send("server: Invalid message")


def check_clients_alive():
    while True:
        for client_id in list(connected_clients.keys()):
            client = connected_clients[client_id]
            if (
                time.time() - client.last_keep_alive
                > clinets_keep_alive_period_in_seconds
            ):
                print("KeepAliveCheck: client", client_id, "got offline!")
                client.send(
                    "server: did not get keep alive in time, closing connection"
                )
                del connected_clients[client_id]
                client.close()

                # notify the clients about the new clients list
                for client_id in list(connected_clients.keys()):
                    connected_clients[client_id].send(
                        "Clients##List " + str(list(connected_clients.keys()))
                    )
        time.sleep(1)
