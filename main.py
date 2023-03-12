#!/usr/bin/env python3

import json
from datetime import datetime, timedelta
from src.sensors.dht22 import *
from src.sensors.relay import *
from src.sensors.soil_moisture import *
from src.sensors.water_level import *
import re
from threading import Timer

import telepot
from telepot.loop import MessageLoop

from src.resources.cred import TOKEN, CHAT_ID

pinOut = {
    "light": 26,
    "dht": 19,
    "soil_moisture": 0,
    "pump": 0,
    "fanOut": 0,
    "fanIn": 0,
    "fanInside": 0,
    "wanter_level": 0
}

def update_status():
    with open('src/resources/status.json', 'w', encoding='utf-8') as f:
        f.write(json.dump(status))
        f.close()

def buildDate(hours, minutes):
    # Get current date and time
    now = datetime.datetime.now()
    
    # Create new datetime with input hours and minutes, and other values from current time
    new_datetime = datetime.datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=hours,
        minute=minutes,
        second=0,
        microsecond=0
    )

    if new_datetime < datetime.datetime.now():
        new_datetime += timedelta(days=1)

    return new_datetime

def init():
    global status, timer_time, bot, light_control, dht, soil_moisture, pump_control, fanOut_control, fanIn_control, water_level, fanInside_control
    with open('src/resources/status.json', 'r', encoding='utf-8') as f:
        status = json.load(f)
    hm = status["startTime"].split(":")
    timer_time = buildDate(hm[0], hm[1])
    bot = telepot.Bot(TOKEN)
    light_control = Relay(pinOut["light"])
    light_control.turnOff()
    dht = DHT22(pinOut["dht"])
    water_level = WaterLever(pinOut["wanter_level"])
    soil_moisture = Soil_Moisture(pinOut["soil_moisture"])
    pump_control = Relay(pinOut["pump"])
    pump_control.turnOn()
    fanOut_control = Relay(pinOut["fanOut"])
    fanOut_control.turnOff()
    fanIn_control = Relay(pinOut["fanIn"])
    fanIn_control.turnOff()
    fanInside_control = Relay(pinOut["fanInside"])
    fanInside_control.turnOff()

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text' and chat_id == CHAT_ID:
        if msg['text'] == "/start":
            welcome = """Welcome farmer to the highest tech growbox\n
                /start --> print welcome messagge\n 
                /info --> print growbox info\n 
                /status --> print relay status\n
                /getCurrentTimer --> print when the light will turn on\n 
                /changeCurrentTimer --> change the time when the light will turn on\n 
                /vegetative --> change to vegetative mode\n 
                /flowering --> change to vegetative mode 
            """
            bot.sendMessage(chat_id, welcome)
        if msg['text'] == "/info":
            try:
                hum, temp = dht.readData()
                soil_moi = soil_moisture.readData()
                info = f'''
                    {"Vegetative" if status["vegetative"] else "Flowering"}\n
                    Temperature: {temp} C\n
                    Humidity: {hum}\n
                    Soil Moisture: {soil_moi}
                '''
                bot.sendMessage(chat_id, info)
            except Exception as e:
                bot.sendMessage(chat_id, e)
        if msg['text'] == "/status":
            info = f'''
                Here the relay status\n
                Light: {light_control.status()}\n
                Pump: {pump_control.status()}\n
                Fan In: {fanIn_control.status()}\n
                Fan Out: {fanOut_control.status()}\n
                Fan Insiede: {fanInside_control.status()}
            '''
            bot.sendMessage(chat_id, info)
        if msg['text'] == "/getCurrentTimer":
            bot.sendMessage(chat_id, f'The light is going to turn ON at {timer_time.strftime("%H:%M")}')
        if '/changeCurrentTimer' in msg['text']:
            rx = re.compile('[0-9]{2}:[0-9]{2}')
            data = rx.search(msg['text'])
            if data:
                status["startTime"] = data.group(1)
                update_status()
                hm = status["startTime"].split(':')
                timer_time = buildDate(hm[0], hm[1])
                bot.sendMessage(chat_id, f'The light is now going to turn ON at {timer_time.strftime("%H:%M")}')
            else:
                bot.sendMessage(chat_id, "Incorrect data format!")

        if msg['text'] == "/vegetative":
            status["vegetative"] = 0
            update_status()
            bot.sendMessage(chat_id, f'Set to vegetative mode')
        if msg['text'] == "/flowering":
            status["vegetative"] = 1
            update_status()
            bot.sendMessage(chat_id, f'Set to flowering mode')
        
def main():
    global timer_time
    MessageLoop(bot, handle).run_as_thread()
    while True:
        if datetime.now() > timer_time:
            if status["vegetative"] == 0 and light_control.status() == 0:
                light_control.turnOn()
                timer_time += timedelta(hours=status["lightHours"]["vegetativeON"])
            if status["vegetative"] == 0 and light_control.status() == 1:
                light_control.turnOff()
                timer_time += timedelta(hours=status["lightHours"]["vegetativeOFF"])
            if status["vegetative"] == 1 and light_control.status() == 0:
                light_control.turnOn()
                timer_time += timedelta(hours=status["lightHours"]["flowering"])
            if status["vegetative"] == 1 and light_control.status() == 1:
                light_control.turnOff()
                timer_time += timedelta(hours=status["lightHours"]["flowering"])
        if water_level.readData() or soil_moisture.readData() == "HIGH":
            pump_control.turnOff()
            t = Timer(1800,pump_control.turnOn(),['Waiting'])
            t.start()
        try:
            hum, temp = dht.readData()
            if  temp < 20 or hum < 40:
                fanIn_control.turnOff()
                fanIn_control.turnOff()
                fanOut_control.turnOff()
                bot.sendMessage(CHAT_ID, f'Temperature or Humidity Too Hight!\nTemperature: {temp} C\nHumidity: {hum} %')
            if temp > 30 or hum > 70:
                fanIn_control.turnOn()
                fanIn_control.turnOn()
                fanOut_control.turnOn()
                bot.sendMessage(CHAT_ID, f'Temperature or Humidity Too Low!\nTemperature: {temp} C\nHumidity: {hum} %')
        except Exception as e:
            bot.sendMessage(CHAT_ID, f'{e}')
        
if __name__ == "__main__":
    init()
    main()