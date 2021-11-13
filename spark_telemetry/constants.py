'''
Table for my reference:

uint8 = B
uint16 = H
uint32 = I
uint64 = Q

float = f

int8 = b
'''

HEADER_SIZE = 192
MOTION_SIZE = 1464
SESSION_SIZE = 251
LAP_DATA_SIZE = 1190
EVENT_SIZE = 35
PARTICIPANTS_SIZE = 1213
CAR_SETUPS_SIZE = 1102
CAR_TELEMETRY_SIZE = 1307
CAR_STATUS_SIZE = 1344
FINAL_CLASSIFICATION_SIZE = 839
LOBBY_INFO_SIZE = 116

HEADER_DATA = '<H4BQfI2B'

packet_ids = dict([
	(0, "motion"),
	(1, "session"),
	(2, "lap_data"),
	(3, "event"),
	(4, "participants"),
	(5, "car_setups"),
	(6, "car_telemetry"),
	(7, "car_status"),
	(8, "final_classification"),
	(9, "lobby_info")
])