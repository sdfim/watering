import time
import json
import requests
import datetime
import math
import sys

from pprint import pprint

s_time = time.time()
path = sys.argv[0].replace('c_timer.py', '')

# скважина качает 4м3/ч или 4000л/ч охватывая 10соток или 1000м2, т.е. за час получается 4л/м2 или 4мм

with open(path+'json/const_zones.json') as f:
  rf = json.load(f)
pprint(rf)
zones = rf['zones']

start_h_watering = rf['start_h_watering']

'''
{
"zones": [
    {"name": "z1",                          # номер/имя зоны полива
    "gpio": "14",                           # gpio esp zone
    "norm": 3,                              # норма суточного полива мм/м2
    "http_esp": "http://192.168.0.54:84"},  # http_esp, возможно подлл. нескольких esp
    {"name": "z2", 
    "gpio": "12", 
    "norm": 3, 
    "http_esp": "http://192.168.0.54:84"}],
"start_h_watering": 19                      # час начала полива
}           
'''

city_openweather = 'Kiev'
api_openweather = 'your_api_key'

#     текущая погода http://api.openweathermap.org/data/2.5/weather?q=Kiev&APPID=your_api_key&units=metric
#     прогноз погоды http://api.openweathermap.org/data/2.5/forecast?q=Kiev&APPID=your_api_key&units=metric
data_weather = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city_openweather+'&APPID='+api_openweather+'&units=metric')
weather = data_weather.json()['list']


today = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
print(today)

cur_time = round(time.time())
print(cur_time)

# считаем суточное количество осадков
day_rain = 0
for d in weather:
    if d['dt'] <= (cur_time+24*60*60) and 'rain' in d:
        print(d['rain'])
        if '3h' in d['rain']: day_rain += d['rain']['3h']

print("day_rain = ", day_rain)
rf.update({"day_rain":day_rain})

temp_time = 0
for z in rf['zones']:
    watering = z["norm"] - day_rain
    if watering > 0:
        h = round(watering/4-watering/4*100%25/100, 2)            # необходимое время полива в часах до сотых
        start_time = round(start_h_watering+temp_time, 2)
        end_time = round(start_h_watering+temp_time+h, 2)
        temp_time += h
        z.update({"watering": [start_time, end_time]})
rf.update({"date":today})
pprint(rf)

with open(path+'json/timer.json', 'w') as outfile:  
    json.dump(rf, outfile)


print("--- %s seconds ---" % (time.time() - s_time))
