# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    weather_geoloc.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aarie-c2@c1r4p1.42sp.org.br <aarie-c2@c    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/02/25 09:46:15 by aarie-c2@c1       #+#    #+#              #
#    Updated: 2025/02/25 11:14:01 by aarie-c2@c1      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import requests

STORMLGLASS_KEY = "7546ea60-f382-11ef-85cb-0242ac130003-7546eace-f382-11ef-85cb-0242ac130003"
OPENCAGE_KEY = "a9b96842e57045e1889f4e3d606e92c7"

def get_lat_lng(location_name):
	opencage_url = "https://api.opencagedata.com/geocode/v1/json"
	params = {
		"q": location_name,
		"key": OPENCAGE_KEY
	}
	response = requests.get(opencage_url, params=params)
	if response.status_code == 200:
		data = response.json()
		if data["results"]:
			lat = data["results"][0]["geometry"]["lat"]
			lng = data["results"][0]["geometry"]["lng"]
			return lat, lng
		else:
			print("Location not found")
			return None, None
	else:
		print("Error with geocoding API:", response.status_code)
		return None, None

def get_weather(lat, lng):
	
	stormglass_url = "https://api.stormglass.io/v2/weather/point"

	params = {
		"lat": lat,
		"lng": lng,
		"params": "airTemperature,humidity,windSpeed,cloudCover,pressure,precipitation",
		"source": "noaa"
	}

	headers = {
		"Authorization": STORMLGLASS_KEY
	}

	response = requests.get(stormglass_url, params=params, headers=headers)

	if response.status_code == 200:
		data = response.json()
		try:
			temperature = data["hours"][0]["airTemperature"]["noaa"]		
			humidity = data["hours"][0]["humidity"]["noaa"]
			wind_speed = data["hours"][0]["windSpeed"]["noaa"]
			cloud_cover = data["hours"][0]["cloudCover"]["noaa"]
			pressure = data["hours"][0]["pressure"]["noaa"]
			precipitation = data["hours"][0]["precipitation"]["noaa"]
		except ValueError:
			print("Error with Stormglass API", response.status_code)
	
		print("Current weather at your location:")
		print("Temperature:", temperature, "ºC")
		print("Humidity:", humidity, "%")
		print("Wind Speed:", wind_speed, "m/s")
		print("Cloud cover:", cloud_cover, "%")
		print("Pressure:", pressure, "hPa")
		print("Precipitation:", precipitation, "mm")
	else:
		print("Error:", response.status_code)
		print("Response content:", response.text)

def main():
	location_name = input("Enter a location name (ex: Vila Madalena, São Paulo):")
	lat, lng = get_lat_lng(location_name)
	if lat is not None and lng is not None:
		get_weather(lat, lng)
	else:
		print("Something went wrong :(")

if __name__ == "__main__":
	main()
	