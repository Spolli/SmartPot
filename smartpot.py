#!/usr/bin/env python3
import serial, json
from datetime import datetime as dt
from time import sleep
from src.utility.utility import *
from src.utility.GPIOutility import *

pinSetup = {
    'PIN_MISC': 13,
    'PIN_WATER_WARM': 12,
    'PIN_VENT_OUT': 11,
    'PIN_VENT_IN': 10,
    'PIN_LAMPS': 9,
    'PIN_POMPA': 8,
    'PIN_DTH22': 7,
    'PIN_WATER_LEVEL': 6,
    'PIN_LIGHT': 5,
    'PIN_WATER_TEMP': 4,
    'PIN_CO2': 3
}

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

plant_info = getDataSheet('src/resources/datasheets/red-hot-chilli-pepper.json')

def checkLight():
    try:
        on = plant_info['growth']['light_hour_on'].split(':')
        off = plant_info['growth']['light_hour_off'].split(':')
        if dt.utcnow().hour == int(on[0]) and dt.utcnow().minute == int(on[1]):
            LampOn()
        if dt.utcnow().hour == int(off[0]) and dt.utcnow().minute == int(off[1]):
            LampOff()
    except Exception as e:
        print(e)

def checkCO2(CO2, TVQ):
    pass

def getSensorValues(line):
    values = line.split(',')
    print(values)

def main():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            getSensorValues(line)
            #checkLight()
            sleep(10)
        
if __name__ == "__main__":
    main()