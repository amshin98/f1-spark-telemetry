# this goes on the EC2 instance

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP

client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.bind(("", 37022))
while True:
   data, addr = client.recvfrom(1024)
   print("received message: %s" % data)