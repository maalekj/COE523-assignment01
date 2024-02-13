import threading


def client_handler(client):
    def handle_message(message):
        # Perform actions based on message content
        if message == "action1":
            # Perform action 1
            pass
        elif message == "action2":
            # Perform action 2
            pass
        else:
            print("Unknown message:", message)
            # Handle unknown message
            pass

    while True:
        message = client.recv(1024).decode()  # Receive client message
        if not message:
            break  # Exit the loop if no message received

        handle_message(message)

    client.close()  # Close the client socket


# Example usage
def run_client_handler(client):
    thread = threading.Thread(target=client_handler, args=(client.client_socket,))
    thread.start()
