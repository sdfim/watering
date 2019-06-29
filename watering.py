import time
import json
import requests
import datetime
import math
import sys

from pprint import pprint

s_time = time.time()

path = sys.argv[0].replace('watering.py', '')
print('path = ',path)

'''
http://192.168.0.54:84/control?cmd=GPIO,14,0           # вкл поток
http://192.168.0.54:84/control?cmd=GPIO,14,1           # выкл поток
http://192.168.0.54:84/control?cmd=status,gpio,14      # состояние
'''

with open(path+'json/timer.json') as f:
  rf = json.load(f)
#pprint(rf)
zones = rf['zones']

start_h_watering = rf['start_h_watering']

c_h = round(int(datetime.datetime.today().strftime('%H'))+int(datetime.datetime.today().strftime('%M'))/60, 2)
print(c_h, datetime.datetime.today().strftime('%H:%M'))


for z in rf['zones']:
    #print(requests.get(http+'/control?cmd=status,gpio,'+z['gpio']).content)
    http = z['http_esp']
    if requests.get(http+'/control?cmd=status,gpio,'+z['gpio']).content == b'?':
        state = 1
    else:
        state = requests.get(http+'/control?cmd=status,gpio,'+z['gpio']).json()['state']
    #print(z['name'], state, z['watering'], c_h)
    if z['watering'][0] <= c_h and z['watering'][1] > c_h and state == 1:
        print("вкл проток зоны", z['name'])
        state = requests.get(http+'/control?cmd=GPIO,'+z['gpio']+',0').json()['state']
    elif (z['watering'][0] > c_h or z['watering'][1] <= c_h) and state == 0:
        print("выкл проток зоны", z['name'])
        state = requests.get(http+'/control?cmd=GPIO,'+z['gpio']+',1').json()['state']
    else:
        print("зона", z['name'], " в норме")
    z.update({"state": state})
pprint(rf)


today = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
rf.update({'date':today})

with open(path+'json/timer.json', 'w') as outfile:  
    json.dump(rf, outfile)


print("--- %s seconds ---" % (time.time() - s_time))
