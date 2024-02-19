import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 9999

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"Server has started...\nConnect with {host} : {port}")

# Lists For Clients
clients = []

def broadcast(message, client):
    # client is current user which we don't want to broadcast
    for c in clients:
        if c != client:
            c.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(4*1024)
            broadcast(message,client)
        except:
            # Removing And Closing Clients
            clients.remove(client)
            client.close()
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"{str(address)} is connected to server")

        clients.append(client)

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
