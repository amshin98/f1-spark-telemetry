# this goes on the EC2 instance

import socket
import struct
import time

from constants import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind(("", 37022))
client.listen()
conn, addr = client.accept()

with conn:
    print("conn by", addr)
    while True:
        data = conn.recv(1024)
        print("received message: %s" % data)
