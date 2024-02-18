import socket
import threading
import cv2
import pickle
import struct
import os


# Function to receive video frames from the server
def receive(client_socket):
    try:
        data = b""
        payload_size = struct.calcsize("Q")
        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024)
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q",packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow("Live Streaming Video Chat",frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        client_socket.close()
    except Exception as e:
        print(f"Error receiving video frame: {e}")

    # Close the OpenCV window and clean up
    cv2.destroyAllWindows()


# Function to send video frames to the server

def send(client, video):
    try:
        while(video.isOpened()):
            ret, frame = video.read()             
            frame = cv2.resize(frame, (320, 320)) 
            frame = cv2.flip(frame, 1)            
                                      
            # sending data to server              
            a = pickle.dumps(frame)               
            message = struct.pack("Q",len(a)) + a 
            client.sendall(message)               
            cv2.imshow("Your Window", frame)                                      
            if cv2.waitKey(1) == ord("q"):        
                break                             
    
        
    except Exception as err:
        raise




#os.environ["QT_QPA_PLATFORM"] = "wayland"
# capturing the video
video = cv2.VideoCapture(0)

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))

# Starting Threads For Listening And Writing
threading.Thread(target=send,args=(client, video, )).start()

#threading.Thread(target=receive,args=(client,)).start()




