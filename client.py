import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ("localhost", 12345)

# Connect to the server
client_socket.connect(server_address)

# Prompt the user for input
message = input("Enter a message to send to the server: ")

# Send data to the server
client_socket.send(message.encode())

# Receive data from the server
data = client_socket.recv(1024)
print("Received from server:", data.decode())

# Close the socket
client_socket.close()
