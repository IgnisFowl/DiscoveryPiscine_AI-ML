# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    weather.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aarie-c2@c1r4p1.42sp.org.br <aarie-c2@c    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/02/25 09:46:15 by aarie-c2@c1       #+#    #+#              #
#    Updated: 2025/02/25 15:12:33 by aarie-c2@c1      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import requests

API_KEY = "7546ea60-f382-11ef-85cb-0242ac130003-7546eace-f382-11ef-85cb-0242ac130003"
url = "https://api.stormglass.io/v2/weather/point"

params = {
	"lat": 91,
	"lng": 182,
	"params": "airTemperature",
	"source": "noaa"
}

headers = {
	"Authorization": API_KEY
}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
	try:
		data = response.json()
	except ValueError:
		print("Response is not valid JSON", response.text)
	temperature = data["hours"][0]["airTemperature"]["noaa"]
	print("Current temperature:", temperature, "ºC")
else:
	print("Error:", response.status_code)
	print("Response content:", response.text)