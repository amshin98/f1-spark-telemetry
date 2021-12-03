import sys
import socket
import time

# Accept data sent from my pc
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Binding to the socket...")
client.bind(("", 37022))
print("Successfully bound!")

client.listen()
conn, addr = client.accept()

with conn:
    print("conn by", addr)
    while True:
        data = conn.recv(4096)
        if len(data) != 0:
            print(data.decode())
            sys.stdout.flush()
