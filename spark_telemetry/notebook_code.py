from pyspark import SparkConf
from pyspark.context import SparkContext

sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))

from pyspark.streaming import StreamingContext

ssc = StreamingContext(sc, 1)
PORT=37023
HOST="localhost"

######################

# Handles empty split pair lines
def split_pair_to_tuple(split_pair):
    if split_pair != None and len(split_pair) == 2:
        lat_val = float(split_pair[0][1:])
        lon_val = float(split_pair[1][0:-1])
        lat_tup = ('lat', (lat_val, 1))
        lon_tup = ('lon', (lon_val, 1))
        return [lat_tup, lon_tup]
    else:
        return [("trash", (0, 1))]
    
# Gets valid averages for lat and lon. In: ('lat', (3.021192053332925, 8))
def get_valid_avg(pre_avg):
    if pre_avg[0] != 'trash':
        return ('valid', (pre_avg[0], pre_avg[1][0] / pre_avg[1][1]))
    else:
        return ('trash', (0, 0))

# Combines valid lat/lon ie ('lon', 0.518593606352806)
def get_valid_lat_lon(a, b):
    lat_val = 0
    lon_val = 0
    if a[0] == 'lat':
        lat_val = a[1]
        lon_val = b[1]
        return (lat_val, lon_val)
    elif a[0] == 'lon':
        lat_val = b[1]
        lon_val = a[1]
        return (lat_val, lon_val)
    else:
        return 0
    
import math

RADIUS = 15


def clamp(n, smallest, largest):
   return max(smallest, min(n, largest))


# val in ab becomes res in cd
# res = (val-A)/(B-A) * (D-C) + C
def interp_single(val, old_min, old_max, new_min, new_max):
   return (val - old_min) / (old_max - old_min) * (new_max - new_min) + new_min


# Takes lat and lon and maps them to int coords in range [1, RADIUS * 2 - 1]
# Note: 0, 0 should give the middle of the range
# Note: Edge of the circle is +/- 4 G
def interp_lat_lon(lat_lon):
   c_lat = clamp(lat_lon[0], -4, 4)
   c_lon = clamp(lat_lon[1], -4, 4)

   new_max = RADIUS * 2 - 1
   i_lat = interp_single(c_lat, -4, 4, 1, new_max)
   i_lon = interp_single(c_lon, -4, 4, new_max, 1)

   return (i_lat, i_lon)


def get_str_circle(center_coords):
   res = ""

   # dist represents distance to the center
   # for horizontal movement
   for i in range((2 * RADIUS)+1):
      # for vertical movement
      for j in range((2 * RADIUS)+1):
         
         # Check draw X
         if j == int(center_coords[0]) and i == int(center_coords[1]):
            res += "X "
         else:
            dist = math.sqrt((i - RADIUS) * (i - RADIUS) + (j - RADIUS) * (j - RADIUS))
  
            if (dist > RADIUS - 0.5 and dist < RADIUS + 0.5):
               res += "*"
            else:
               res += "  "
      res += "\n"

   return res


'''
Takes a (val?, (lat, lon)) tuple then returns a string ASCII art representing the g force
Input: ('valid', (-0.1252590595977381, 0.4670624114573002)) or ('trash', (0, 0))
'''
def get_g_force_ind(pot_vals):
   if pot_vals[0] == "trash":
      return ""
   else:
      lat = pot_vals[1][0]
      lon = pot_vals[1][1]
      lat_lon = (lat, lon)
      i_lat_lon = interp_lat_lon(lat_lon)
      return get_str_circle(i_lat_lon)


# Read in the double space-separated g force data
g_forces = ssc.socketTextStream(HOST, PORT)

avg_g_forces = g_forces.flatMap(lambda forces: forces.split("  "))\
                       .map(lambda pair: pair.split(","))\
                       .flatMap(split_pair_to_tuple)\
                       .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))\
                       .map(get_valid_avg)\
                       .reduceByKey(get_valid_lat_lon)\
                       .map(get_g_force_ind)

avg_g_forces.pprint()


ssc.start()
ssc.awaitTerminationOrTimeout(30) # wait 60 seconds