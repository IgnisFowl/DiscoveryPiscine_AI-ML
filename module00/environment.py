# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    environment.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aarie-c2@c1r4p1.42sp.org.br <aarie-c2@c    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/02/24 10:25:05 by aarie-c2@c1       #+#    #+#              #
#    Updated: 2025/02/24 11:08:00 by aarie-c2@c1      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import time
import math
import random

SEASON_TEMP = {
	"winter": (-5, 10),
	"spring": (5, 20),
	"summer": (15, 35),
	"fall": (5, 18)
}

'''
math.sin(math.pi * hour / 24): The sine function takes an angle (in radians). By multiplying hour / 24 by π (pi), you ensure the temperature follows a full cycle from 0 to 23 hours. The sine wave goes from -1 to 1 over 24 hours, which will give us values oscillating around the midpoint (mid_temp).
Morning: Around hour 6, the sine wave starts rising.
Noon: Around hour 12, the sine wave reaches the peak (+1).
Evening: Around hour 18, it starts decreasing.
Midnight: Around hour 24, it goes back to its lowest point (-1).
'''

def get_temperature(hour, min_temp, max_temp):
	mid_temp = (max_temp + min_temp) / 2
	amplitude = (max_temp - min_temp) / 2
	temp = mid_temp + amplitude * math.sin(math.pi * hour / 24)
	temp += random.uniform(-0.5, 0.5)
	return round(temp, 2)

def simulate_day(season):
	if season not in SEASON_TEMP:
		print("Invalid season, please choose from: winter, spring, summer, fall.")
		return
	
	min_temp, max_temp = SEASON_TEMP[season]

	print(f"Simulating a day in {season}...")

	for time_slice in range(48):
		hour = (time_slice / 2)
		temp = get_temperature(hour, min_temp, max_temp)
		print(temp)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python3 environment.py <season>")
		sys.exit(1)
	
	season = sys.argv[1].lower()
	simulate_day(season)