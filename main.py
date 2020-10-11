import requests
import sqlite3


def save_earthquakes(custom_eq_list):
	conn = sqlite3.connect('earthquakes_db.db')
	cursor = conn.cursor()
	while True:
		try:
			quakes = input('Enter name of Table: ')
			cursor.execute(f"CREATE TABLE {quakes} (count INTEGER, place TEXT, magnitude REAL);")
			break
		except Exception:
			print('Please create any name')
			continue
	cursor.executemany(f'INSERT INTO {quakes} VALUES (?, ?, ?);', custom_eq_list)
	conn.commit()
	conn.close()


count = 0
custom_earthquake_list = []
url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'

start_time = input('Enter the start time: ')
end_time = input('Enter the end time: ')
latitude = input('Enter the latitude: ')
longitude = input('Enter the longitude: ')
max_radius_km = input('Enter the max radius in km: ')
min_magnitude = input('Enter the min magnitude: ')

response = requests.get(url, headers={'Accept':'application/json'}, params={
		'format':'geojson',
		'starttime':start_time,
		'endtime':end_time,
		'latitude':latitude,
		'longitude':longitude,
		'maxradiuskm':max_radius_km,
		'minmagnitude':min_magnitude
	})
	
data = response.json()
earthquake_list = data['features']

for earthquake in earthquake_list:
    count += 1
    custom_earthquake_list.append((count, earthquake['properties']['place'], earthquake['properties']['mag']))

save_earthquakes(custom_earthquake_list)