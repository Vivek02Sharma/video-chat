import socket,cv2, pickle,struct,threading

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST_IP = '127.0.0.1'
print(HOST_IP)
PORT = 9999
server.bind((HOST_IP,PORT))
server.listen(5)

print("Server has started\n")
def show_client(client,addr):
    try:
        print(f"Client {addr} is Connected")
        if client:
            data = b""
            payload_size = struct.calcsize('Q')
            while True:
                while len(data) < payload_size:
                    packet = client.recv(4*1024)
                    if not packet:break
                    data += packet
                packet_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack('Q',packet_msg_size)[0]

                while len(data) < msg_size:
                    data += client.recv(4*1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                cv2.imshow(f"Video from {addr}",frame)
                if cv2.waitKey(1) == ord('q'):
                    break
            client.close()

    except Exception as e:
        print(f"Client {addr} is Disconnected")
        print(f"Total client connection is {threading.active_count() - 2}\n")
        pass

while True:
    client,addr = server.accept()
    thread = threading.Thread(target=show_client,args=(client,addr))
    thread.start()
    print(f"Total client connection is {threading.active_count() - 1}\n")



