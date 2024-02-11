import socket,cv2, pickle,struct

video = cv2.VideoCapture(0)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST_IP = '0.tcp.in.ngrok.io'
PORT = 17634
client.connect((HOST_IP,PORT))

if client:
    while(video.isOpened()):
        try:
            ret,frame = video.read()
            frame = cv2.resize(frame,(320,320))
            frame = cv2.flip(frame,1)
            a = pickle.dumps(frame)
            msg = struct.pack("Q",len(a))+a
            client.sendall(msg)
            cv2.imshow('Client Window',frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                client.close()
        except Exception as e:
            raise(e)
        

