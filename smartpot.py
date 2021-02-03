#!/usr/bin/env python3
import json
from datetime import datetime as dt
from time import sleep
from src.sensors import *

with open('/home/spolli/DevSpace/Python-project/SmartPot/src/resources/status.json', 'r', encoding='utf-8') as f:
    status = json.load(f) 

def update_status():
    with open('/home/spolli/DevSpace/Python-project/SmartPot/src/resources/status.json', 'w', encoding='utf-8') as f:
        f.write(json.dump(status))
        f.close()

def checkLight(rele):
    global status
    on = plant_info['growth']['light_hour_on']
    off = plant_info['growth']['light_hour_off']
    if dt.utcnow().hour == int(on[0]) and status['LAMPS'] == 0:
        rele.turnOn('LAMPS')
        status['LAMPS'] = 1
        update_status()
    if dt.utcnow().hour == int(off[0]) and status['LAMPS'] == 1:
        rele.turnOff('LAMPS')
        status['LAMPS'] = 0
        update_status()

def main():
    rele = Relay()
    wat_level_in = WaterLever(9)
    wat_level_out = WaterLever(11)
    sensors = [DHT22(7), Ds18(), LM333(8)]
    while True:
        data = []
        for sen in sensors:
            data.append(sen.readData())
        #TODO upload sensor data to db to statistics
        if wat_level_out.readData() == 0:
            #TODO send telegram message to refill tank
        checkLight(rele)
        
        sleep(20)
        
if __name__ == "__main__":
    main()