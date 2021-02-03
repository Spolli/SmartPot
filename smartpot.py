#!/usr/bin/env python3
import json
from datetime import datetime as dt
from time import sleep
from src.sensors import *

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

def main():
    while True:
        pass
        
if __name__ == "__main__":
    main()