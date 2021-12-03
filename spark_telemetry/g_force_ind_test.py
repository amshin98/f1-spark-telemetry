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


def print_circle(center_coords):
   # dist represents distance to the center
   # for horizontal movement
   for i in range((2 * RADIUS)+1):
      # for vertical movement
      for j in range((2 * RADIUS)+1):
         
         # Check draw X
         if j == int(center_coords[0]) and i == int(center_coords[1]):
            print("X ", end="")
         else:
            dist = math.sqrt((i - RADIUS) * (i - RADIUS) + (j - RADIUS) * (j - RADIUS))
  
            if (dist > RADIUS - 0.5 and dist < RADIUS + 0.5):
               print("*",end="")
            else:
               print("  ",end="")
      print()


def get_g_force_ind(pot_vals):
   if pot_vals[0] == "trash":
      return ""
   else:
      lat = pot_vals[1][0]
      lon = pot_vals[1][1]
      lat_lon = (lat, lon)
      i_lat_lon = interp_lat_lon(lat_lon)
      print_circle(i_lat_lon)


if __name__ == "__main__":
   get_g_force_ind(('valid', (1.2, 1.8)))