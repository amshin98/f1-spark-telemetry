import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

server.setsockopt(socket.SOL_SOCKET, socket. SO_BROADCAST, 1)

server.settimeout(0.2)
message = b"{t:1, a:2, c:3}"

dest = ("50.17.28.224", 37022)
while True:
   server.sendto(message, dest)
   print("sent", flush=True)
   time.sleep(0.01)