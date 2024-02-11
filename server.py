import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST_IP = '127.0.0.1'
print(HOST_IP)
PORT = 9999
server.bind((HOST_IP, PORT))
server.listen(5)

print("Server has started\n")

def show_client(client, addr):
    try:
        print(f"Client {addr} is Connected")
        if client:
            while True:
                data = client.recv(4 * 1024)
                if not data:
                    break
                client.sendall(data)
    except Exception as e:
        print(f"Exception occurred with client {addr}: {e}")
    finally:
        print(f"Client {addr} is Disconnected")
        print(f"Total client connections: {threading.active_count() - 2}\n")
        client.close()

while True:
    client, addr = server.accept()
    thread = threading.Thread(target=show_client, args=(client, addr))
    thread.start()
    print(f"Total client connections: {threading.active_count() - 1}\n")
