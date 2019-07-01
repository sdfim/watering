import time
import json
import requests
import datetime
import math
import sys

from pprint import pprint

import relay

s_time = time.time()

path = sys.argv[0].replace('watering.py', '')
print('path = ',path)

'''
http://192.168.0.54/control?cmd=GPIO,14,0           # вкл поток, реле NO
http://192.168.0.54/control?cmd=GPIO,14,1           # выкл поток
http://192.168.0.54/control?cmd=status,gpio,14      # состояние
'''

with open(path+'json/timer.json') as f:
  rf = json.load(f)
#pprint(rf)
zones = rf['zones']

start_h_watering = rf['start_h_watering']

c_h = round(int(datetime.datetime.today().strftime('%H'))+int(datetime.datetime.today().strftime('%M'))/60, 2)
print(c_h, datetime.datetime.today().strftime('%H:%M'))


for z in rf['zones']:
    
    # gpio on esp
    if 'http_esp' in z:
        http = z['http_esp']
        response = requests.get(http+'/control?cmd=status,gpio,'+z['gpio'])
        i = 0
        while response.status_code != 200 or i > 5:
            i += 1
            response = requests.get(http+'/control?cmd=status,gpio,'+z['gpio'])
            
        print(response.status_code, i)
        print(response.content)
        print(response.json())
        if response.content == b'?':
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
            
    # gpio on raspberry pi
    else:
        state = relay.status_relay(z['gpio'])
        if z['watering'][0] <= c_h and z['watering'][1] > c_h and state == 1:
            print("вкл проток зоны", z['name'])
            state = relay.on_relay(z['gpio'])
            state = relay.status_relay(z['gpio'])
        elif (z['watering'][0] > c_h or z['watering'][1] <= c_h) and state == 0:
            print("выкл проток зоны", z['name'])
            state = relay.off_relay(z['gpio'])
            state = relay.status_relay(z['gpio'])
        else:
            print("зона", z['name'], " в норме")
            
    z.update({"state": state})
pprint(rf)


today = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
rf.update({'date':today})

with open(path+'json/timer.json', 'w') as outfile:  
    json.dump(rf, outfile)


print("--- %s seconds ---" % (time.time() - s_time))
