import socket
import json

# Create a server socket and listen for incoming connections
host = 'localhost'
port = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()

# Accept a client connection
print(f'Listening for client connections on {host}:{port}...')
conn, addr = s.accept()
print(f'Client connected from {addr[0]}:{addr[1]}')

# Receive and process data from client
while True:
    data = conn.recv(1024)
    if not data:
        break
    # Decode the JSON string to a Python dictionary
    json_data = json.loads(data.decode())
    # Process the data as needed
    print(json_data)

# Close the connection
conn.close()
