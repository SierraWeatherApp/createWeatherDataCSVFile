import requests
import json
import csv
import os

fileout = 'output/output.csv'
if os.path.exists(fileout):
    os.remove(fileout)
    # Berlin, Hong Kong, Beijing, Grumantbreen, Hammarfest, Nguru, cape town, punta arenas, cuiaba, dariyah, mumbai, sangla, bankok
cities = [[52.52, 13.41], [22.27, 114.17], [39.90, 116.39], [78.15, 15.23], [70.68, 23.67], [12.87, 10.45], [-33.92, 18.42], [-53.14, -70.91], [-15.59, -56.09], [24.73, 42.91], [19.07, 72.88], [31.42, 26.20], [13.75, 100.50] ]
users = [{'sandalUser': True, 'shortUser': True, 'capUser': True, 'userPlace': 5, 'userTemp': 3},
         {'sandalUser': False, 'shortUser': False, 'capUser': False, 'userPlace': -5, 'userTemp': 3},
         {'sandalUser': False, 'shortUser': False, 'capUser': True, 'userPlace': 5, 'userTemp': 3},
         {'sandalUser': False, 'shortUser': True, 'capUser': False, 'userPlace': -5, 'userTemp': -3},
         {'sandalUser': False, 'shortUser': False, 'capUser': False, 'userPlace': 5, 'userTemp': -3},
         {'sandalUser': False, 'shortUser': False, 'capUser': False, 'userPlace': -5, 'userTemp': -3}]
#apperent_temperature, pricipitation_probability
def recommender(temp, rain_prop, sandalUser, shortUser, capUser, userOffset):
    rain = False
    if(rain_prop > 40):
        rain = True
    temp += userOffset

    if capUser:
        head = "cap"
    else:
        head = "empty"

    if sandalUser:
        shoes = "sandals"
    else:
        shoes = "sneakers"

    if shortUser:
        pants = "shorts"
    else:
        pants = "pants"

    if temp < -10:
        head = "beanie"
        shirt = "hoodie"
        jacket = "winter"
        pants = "snow-pants"
        shoes = "boots"

    elif temp < 0:
        head = "beanie"
        shirt = "hoodie"
        jacket = "winter"
        pants = "pants"
        shoes = "boots"

    elif temp < 8:
        shirt = "hoodie"
        jacket = "winter"
        pants = "pants"
        shoes = "sneakers"

    elif temp < 14:
        shirt = "hoodie"
        jacket = "light"
        pants = "pants"
        shoes = "sneakers"

    elif temp < 18:
        shirt = "hoodie"
        jacket = "empty"
        pants = "pants"
        shoes = "sneakers"

    elif temp < 22:
        shirt = "long-sleeve"
        jacket = "empty"
        pants = "pants"
        shoes = "sneakers"

    elif temp < 26:
        shirt = "t-shirt"
        jacket = "empty"
        pants = "pants"

    else:
        head = "cap"
        shirt = "t-shirt"
        jacket = "empty"

    if rain and temp > 5:
        umbrella = True
        shoes = "rain-boots"
    else:
        umbrella = False

    return {'head': head, 'shirt': shirt, 'jacket': jacket, 'pants': pants, 'shoes': shoes, 'umbrella': umbrella}
def writetoFile(data):
    fieldnames = ['apparent_temperature', 'temperature_2m', 'relativehumidity_2m', 'windspeed_10m',
                  'precipitation_probability', 'direct_radiation',
                  'head', 'shirt', 'jacket', 'pants', 'shoes', 'umbrella',
                  'sandalUser', 'shortUser', 'capUser', 'userPlace', 'userTemp']
    if os.path.exists(fileout):
       with open(fileout, 'r') as infile, open(fileout, 'a', newline='') as outfile:
           writer = csv.DictWriter(outfile, fieldnames=fieldnames)
           for row in data:
               writer.writerow(row)
    else:
        with open(fileout, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
def getWeather(lat, long):
    url = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=" + str(long) + "&hourly=temperature_2m"
    response = requests.get('https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&forecast_days=1&hourly=apparent_temperature,temperature_2m,relativehumidity_2m,windspeed_10m,precipitation_probability,direct_radiation')
    jsonResponse = json.loads(response.content)['hourly']
    apparent_temperature = jsonResponse['apparent_temperature']
    temperature_2m = jsonResponse['temperature_2m']
    relativehumidity_2m = jsonResponse['relativehumidity_2m']
    windspeed_10m = jsonResponse['windspeed_10m']
    precipitation_probability = jsonResponse['precipitation_probability']
    direct_radiation = jsonResponse['direct_radiation']
    data = []
    for i in range(len(apparent_temperature)):
        for user in users:
            clothingRec = recommender(apparent_temperature[i], precipitation_probability[i], user['sandalUser'], user['shortUser'], user['capUser'], user['userPlace'] + user['userTemp'])
            data.append({'apparent_temperature': apparent_temperature[i],'temperature_2m': temperature_2m[i],'relativehumidity_2m': relativehumidity_2m[i],
                         'windspeed_10m': windspeed_10m[i],'precipitation_probability': precipitation_probability [i],'direct_radiation': direct_radiation[i],
                         'head': clothingRec['head'],'shirt': clothingRec['shirt'], 'jacket': clothingRec['jacket'], 'pants': clothingRec['pants'], 'shoes': clothingRec['shoes'],
                         'umbrella': clothingRec['umbrella'],
                         'sandalUser': user['sandalUser'], 'shortUser': user['shortUser'], 'capUser': user['capUser'], 'userPlace': user['userPlace'], 'userTemp':  user['userTemp']})
    writetoFile(data)
for city in cities:
    getWeather(city[0], city[1])