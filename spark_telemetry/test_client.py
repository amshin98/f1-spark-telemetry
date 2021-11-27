# this goes on the EC2 instance

import socket
import struct
import time

from constants import *

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP

client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("Binding...")
client.bind(("", 37022))
print("Successfully bound!")

while True:
   data, addr = client.recvfrom(MOTION_SIZE)
   unpacked = struct.unpack_from(HEADER_DATA, data)
   packet_type = unpacked[4]
   #print("=======================\n", unpacked, struct.calcsize(HEADER_DATA))
   # Only read session (1), telemetry (6), and lap data (2) packets
   # Session
   if packet_type == 1:
      session_data = struct.unpack_from(SESSION_DATA, data, offset=HEADER_SIZE)
      track_temp = session_data[1]
      air_temp = session_data[2]

      print("======================================")
      print("SESSION")
      print(track_temp, air_temp)
   # Telemetry
   elif packet_type == 6:
      car_idx = unpacked[8]
      start_idx = NUM_CTD_ENTRIES * car_idx
      telemetry_data = struct.unpack_from(TELEMETRY_DATA, data, offset=HEADER_SIZE)
      brake_temps = telemetry_data[start_idx + 9: start_idx + 13]
      tire_surface_temps = telemetry_data[start_idx + 13: start_idx + 17]
      tire_carcass_temps = telemetry_data[start_idx + 17: start_idx + 21]

      print("======================================")
      print("TEL")
      print("brakes\n", brake_temps)
      print("surface\n", tire_surface_temps)
      print("carcass\n", tire_carcass_temps)
   # Lap data
   elif packet_type == 2:
      car_idx = unpacked[8]
      start_idx = NUM_LDS_ENTRIES * car_idx
      lap_data_data = struct.unpack_from(LAP_DATA_DATA, data, offset=HEADER_SIZE)
      last_lap_time = lap_data_data[start_idx]
      cur_lap_time = lap_data_data[start_idx + 1]

      print("======================================")
      print("LAP DATA")
      print(unpacked)
      print(last_lap_time, cur_lap_time)

   #print(unpacked)
   #print("received message: %s" % header)
   #print("===============================")
   #time.sleep(0.5)


   #print(packet_ids[unpacked[4]])
   

