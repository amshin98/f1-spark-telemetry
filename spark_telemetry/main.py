import socket
import struct
import time

from constants import *

# How often to send packets to the server
SEND_HZ = 1
SLEEP_TIME = 1.0 / SEND_HZ

def current_milli_time():
   return round(time.time() * 1000)

def main():

   # Connect to F1 2020
   client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 
   client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

   print("Binding to F1 2020...")
   client.bind(("", 37022))
   print("Successfully bound!")

   # Connect to the class server
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   dest = ("127.0.0.1", 5050)
   print("Connecting to the class server...")
   server.connect(dest)
   print("Connected!")

   # Keep track of how long since the last packet's been sent
   last_sent_time = current_milli_time()

   # List of (lat, lon) G forces to be sent as a packet
   g_forces = []

   # Continually receive game packets
   while True:
      data, addr = client.recvfrom(MOTION_SIZE)
      unpacked = struct.unpack_from(HEADER_DATA, data)

      packet_type = unpacked[4]

      # Only read motion packets
      if packet_type == 0:
         car_idx = unpacked[8]
         start_idx = NUM_CMD_ENTRIES * car_idx

         motion_data = struct.unpack_from(MOTION_DATA, data, offset=HEADER_SIZE)
         lat_g = motion_data[start_idx + 12]
         lon_g = motion_data[start_idx + 13]
         #print(lat_g, lon_g)
         g_forces.append(str((lat_g, lon_g)))

      # Check if we want to send the packet to the server
      if current_milli_time() - last_sent_time >= 1000:
         # Double-space separated
         message = "  ".join(g_forces) + "\n"
         server.sendall(message.encode('UTF-8'))

         g_forces = []
         last_sent_time = current_milli_time()
         print("sent")

if __name__ == '__main__':
    main()