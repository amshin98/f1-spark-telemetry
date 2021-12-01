'''
Table for my reference:

uint8 = B
uint16 = H
uint32 = I
uint64 = Q

float = f

int8 = b
'''

# All in bytes
HEADER_SIZE = 24
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

MARSHAL_ZONE_DATA = 'fb'
WEATHER_FORECAST_SAMPLE_DATA = '3B2b'
SESSION_DATA = '<B2bBHBbB2H6B'# + (21 * MARSHAL_ZONE_DATA) + '3B' \
#	+ (20 * WEATHER_FORECAST_SAMPLE_DATA)

CAR_TELEMETRY_DATA = 'H3fBbH2B4H8BH4f4B'
NUM_CTD_ENTRIES = 30
TELEMETRY_DATA = '<' + (22 * CAR_TELEMETRY_DATA) + "I2Bb"

LAP_DATA_STRUCT_DATA = '2f2HfB4HBHBHB3f9B'
NUM_LDS_ENTRIES = 27
LAP_DATA_DATA = '<' + (22 * LAP_DATA_STRUCT_DATA)

CAR_MOTION_DATA_DATA = '6f6h6f'
NUM_CMD_ENTRIES = 18
MOTION_DATA = '<' + (22 * CAR_MOTION_DATA_DATA) + '30f'

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