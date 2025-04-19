import socket
import os

PORT = 9999
SERVER = '107.23.250.168'
#SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Client.connect(ADDR)

DOWNLOADING = False

def send(msg):
    msg = str(msg)
    Message = msg.encode('utf-8')
    msg_length = len(Message)
    send_length = str(msg_length).encode('utf-8')
    send_length += b' '*(64-len(send_length))
    Client.send(send_length)
    Client.send(Message)

def recv():
    msg_length = Client.recv(64).decode('utf-8')
    print(f"Received msg_length: {msg_length}")
    if msg_length:
        try:
            msg_length = int(msg_length)
        except ValueError:
            print(f"Invalid msg_length value: {msg_length}")
            return None
        received_data = b''
        while len(received_data) < msg_length:
            chunk = Client.recv(1)
            if not chunk:
                break
            received_data += chunk
            print(f"Received {len(received_data)} bytes out of {msg_length}")
        if DOWNLOADING == True:
            send('DONE')
        return received_data
    else:
        return None



send('INSTALL')
send('DONE')
while True:
    file_type = recv()
    name = recv()
    DOWNLOADING = True
    msg = recv()
    DOWNLOADING = False
    if msg == b'DONE' or name == b'DONE' or file_type == b'DONE':
        break
    elif file_type == b'FOLDER':
        name = name.decode('utf-8')
        try:
            os.mkdir(name)
        except FileExistsError:
            pass
        os.chdir(name)
    elif file_type == b'FILE':
        with open(name, 'wb') as file:
            file.write(msg)
            

            