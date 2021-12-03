import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dest = ("127.0.0.1", 5050)
server.connect(dest)

message = b"{t:1, a:2, c:3}"
while True:
   server.sendall(message)
   print("sent", flush=True)
   time.sleep(0.1)