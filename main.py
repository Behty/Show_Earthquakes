import requests
import sqlite3

url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'
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
count = 0
insert_query = f'INSERT INTO {quakes} VALUES (?, ?, ?);'

for earthquake in earthquake_list:
    count += 1
	# print(f"{count}. Place: {earthquake['properties']['place']}. Magnitude: {earthquake['properties']['mag']}.")
    cursor.execute(insert_query, (count, earthquake['properties']['place'], earthquake['properties']['mag']))

conn.commit()
conn.close()
