# this goes on the EC2 instance

import socket
import struct
import time

from constants import *

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP

client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.bind(("", 37022))

while True:
   data, addr = client.recvfrom(MOTION_SIZE)
   print(struct.unpack_from(HEADER_DATA, data))
   #print("received message: %s" % header)
   print("===============================")
   time.sleep(0.5)