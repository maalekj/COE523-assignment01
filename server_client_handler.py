import pickle
import threading
import time

# shared data with all clients handlers
connected_clients = {}
clinets_keep_alive_period_in_seconds = 10

connected_clients_lock = threading.Lock()
client_sending_lock = threading.Lock()


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
                message = self.client_socket.recv(255)
                message = pickle.loads(message)
            except ConnectionResetError and OSError:
                pass
            if message == "":
                print("Client socket of client" + self.client_id + "is None, exiting")
                self.close()
                time.sleep(1)
                return

            self.handle_message(str(message))

    def send(self, message):
        client_sending_lock.acquire()
        self.client_socket.send(pickle.dumps(message))
        client_sending_lock.release()

    def receive(self):
        return self.client_socket.recv(255)

    def close(self):
        self.client_socket.close()

    def handle_message(self, message):
        # Perform actions based on message content
        if message[:8] == "Connect " and len(message) >= 8:
            if self.client_id is not None:
                self.send("server: You are already connected!")
                return
            self.client_id = message[8:]
            connected_clients_lock.acquire()
            connected_clients[self.client_id] = self
            connected_clients_lock.release()
            # notify the client that it is connected and the keep alive period that the client should send whithin to be considered alive
            self.send("KEEPALIVE##" + str(clinets_keep_alive_period_in_seconds))

        elif message == "Quit " + self.client_id:
            print("client", self.client_id, "is quitting")

            connected_clients_lock.acquire()
            # remove the client from the connected_clients dictionary
            if self.client_id in connected_clients:
                del connected_clients[self.client_id]
            connected_clients_lock.release()

            # notify the clients about the new clients list
            for client_id in list(connected_clients.keys()):
                connected_clients[client_id].send(
                    "Clients##List" + str(list(connected_clients.keys()))
                )
            self.close()

        elif message == "List":

            # send the connected clients list
            self.send("Clients##List" + str(list(connected_clients.keys())))

        elif message == "Alive":
            # update the last keep alive time
            self.last_keep_alive = time.time()

        elif " " in message:
            # message structured should be: first 8 bytes are the receiver id, then 8 bytes for sender id, then the message
            receiver_id = message[:8].split(" ")[0]
            sender_id = message[8:16].split(" ")[0]
            message = message[16:]

            if sender_id != self.client_id:
                self.send("server: Invalid sender id")
                return

            connected_clients_lock.acquire()
            if receiver_id in connected_clients:
                connected_clients[receiver_id].send(self.client_id + ":" + message)
            else:
                self.send("server: Client " + receiver_id + " is not connected")
            connected_clients_lock.release()

        else:
            self.send("server: Invalid message")


def check_clients_alive():
    while True:
        connected_clients_lock.acquire()
        for client_id in list(connected_clients.keys()):
            client = connected_clients[client_id]
            if (
                time.time() - client.last_keep_alive
                > clinets_keep_alive_period_in_seconds
            ):
                print("KeepAliveCheck: client", client_id, "got offline!")
                try:

                    client.send(
                        "server: did not get keep alive in time, closing connection"
                    )
                except BrokenPipeError:
                    pass
                del connected_clients[client_id]
                client.close()

                # notify the clients about the new clients list
                for client_id in list(connected_clients.keys()):
                    connected_clients[client_id].send(
                        "Clients##List" + str(list(connected_clients.keys()))
                    )
        connected_clients_lock.release()
        time.sleep(1)


def num_of_connected_clients():
    # return number of connected clients
    return len(connected_clients)
