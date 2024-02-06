import socket
import struct

port = 9090
server = "localhost"

# Build server to receive objectoutputstream from java client
SERVER = socket.gethostbyname(server)
ADDR = (SERVER, port)
HEADER = 8  # Assuming the length is an 8-byte integer
FORMAT = '!Q'  # 'Q' represents an unsigned long long (8 bytes)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(ADDR)
s.listen(5)

while True:
    conn, addr = s.accept()
    print(f"[NEW CONNECTION] {addr} connected.")

    msg_length_data = b''
    while len(msg_length_data) < HEADER:
        print("Waiting for message length data ... ")
        chunk = conn.recv(HEADER - len(msg_length_data))
        print("Chunk: ", chunk)
        if not chunk:
            break
        msg_length_data += chunk

    print(f"Received {len(msg_length_data)} bytes of message length data.")

    if len(msg_length_data) == HEADER:
        print("Message length data received.")
        msg_length = struct.unpack(FORMAT, msg_length_data)[0]
        print(f"Message length: {msg_length}")

        msg = b''
        while len(msg) < msg_length:
            print("Waiting for message ... ")
            chunk = conn.recv(min(msg_length - len(msg), 4096))
            if not chunk:
                break
            msg += chunk
            print("Message: ", msg)

        if len(msg) == msg_length:
            print("Message received.")
            msg = msg.decode('utf-8')
            print(f"[{addr}] {msg}")
            if msg == "si_":
                print("SIMULATE")
            else:
                print(msg)
        else:
            print("Error receiving complete message.")
    else:
        print("Error receiving message length.")
