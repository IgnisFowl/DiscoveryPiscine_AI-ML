# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    expert_system.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aarie-c2@c1r4p1.42sp.org.br <aarie-c2@c    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/02/24 10:38:56 by aarie-c2@c1       #+#    #+#              #
#    Updated: 2025/02/24 10:59:02 by aarie-c2@c1      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

def regulate_temp(min_temp, max_temp):
	indoor_temp = None

	for line in sys.stdin:
		try:
			external_temp = float(line.strip())
		except ValueError:
			continue
	
		if indoor_temp is None:
			indoor_temp = external_temp
		
		if indoor_temp < min_temp:
			action = "heating"
			indoor_temp += 0.5
		elif indoor_temp > max_temp:
			action = "cooling"
			indoor_temp -= 0.5
		else:
			action = "nothing"
			
			if indoor_temp < external_temp:
				indoor_temp += 0.25
			elif indoor_temp > external_temp:
				indoor_temp -= 0.25
		
		print(f"{external_temp:.2f} - {action} - {indoor_temp:.2f}")
	
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python3 environment.py <season> | expert_system.py <min_temp> <max_temp>")
		sys.exit(1)
	
	try:
		min_temp = float(sys.argv[1])
		max_temp = float(sys.argv[2])
	except ValueError:
		print("Error: min_temp and max_temp must be numbers.")
		sys.exit(1)
	
	regulate_temp(min_temp, max_temp)