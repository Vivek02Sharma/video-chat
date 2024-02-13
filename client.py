import socket
import cv2
import pickle
import struct

video = cv2.VideoCapture(0)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST_IP = '127.0.0.1'
PORT = 9999
client.connect((HOST_IP, PORT))

while True:
    try:
        ret, frame = video.read()
        frame = cv2.resize(frame, (320, 320))
        frame = cv2.flip(frame, 1)
        data = pickle.dumps(frame)
        message = struct.pack("Q", len(data)) + data
        client.sendall(message)
         cv2.imshow("Your Window", frame)
        
        data = b""
        payload_size = struct.calcsize("Q")
        while len(data) < payload_size:
            packet = client.recv(4 * 1024)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client.recv(4 * 1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("Other Client Window", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    except Exception as e:
        print(f"Error: {e}")
        break

video.release()
cv2.destroyAllWindows()
client.close()
