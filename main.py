#!/usr/bin/env python3

import json
from datetime import datetime
from time import sleep

import telepot
from telepot.loop import MessageLoop
from src.resources.config import PIN_CONFIG, TOKEN, CHAT_ID
from src.sensors.dht22 import DHT22
from src.sensors.relay import Relay
from src.sensors.soil_moisture import Soil_Moisture
from src.sensors.water_level import WaterLever

PIN_CONFIG = {
    "light": 26,
    "dht": 19,
    "soil_moisture": 13,
    "pump": 21,
    "fanOut": 20,
    "fanIn": 16,
    "fanInside": 12,
    "wanter_level": 25
}

DEBUG = True

def update_status(status_data):
    try:
        with open('src/resources/status.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(status_data))
    except Exception as e:
        raise ValueError(f"Error updating status: {str(e)}")

def init():
    global status, bot, light_control, dht, soil_moisture, pump_control, fanOut_control, fanIn_control, water_level, fanInside_control
    with open('src/resources/status.json', 'r', encoding='utf-8') as f:
        status = json.load(f)
    bot = telepot.Bot(TOKEN)
    light_control = Relay(PIN_CONFIG["light"])
    light_control.turnOff()
    dht = DHT22(PIN_CONFIG["dht"])
    water_level = WaterLever(PIN_CONFIG["wanter_level"])
    soil_moisture = Soil_Moisture(PIN_CONFIG["soil_moisture"])
    pump_control = Relay(PIN_CONFIG["pump"])
    pump_control.turnOn()
    fanOut_control = Relay(PIN_CONFIG["fanOut"])
    fanOut_control.turnOff()
    fanIn_control = Relay(PIN_CONFIG["fanIn"])
    fanIn_control.turnOff()
    fanInside_control = Relay(PIN_CONFIG["fanInside"])
    fanInside_control.turnOff()

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if DEBUG:
        print(content_type, chat_type, chat_id)
    if content_type == 'text':
        if msg['text'] == "/start":
            welcome = '''Welcome farmer to the highest tech growbox
/start --> print welcome messagge
/sensors --> print growbox sensors's infos
/status --> print relay status
/getCurrentTimer --> print when the light will turn on
/changeStartTime --> change the time when the light will turn on
/changeEndTime --> change the time when the light will turn off
            '''
            bot.sendMessage(chat_id, welcome)
        if msg['text'] == "/sensors":
            try:
                hum, temp = dht.readData()
                soil_moi = soil_moisture.readData()
                info = f'''
Temperature: {temp:.2f} ºC
Humidity: {hum:.2f} %
Soil Moisture: {soil_moi}
                '''
                bot.sendMessage(chat_id, info)
            except Exception as e:
                if DEBUG:
                    print(f"Error reading sensors: {e}")
                else:
                    bot.sendMessage(chat_id, "An error occurred while reading sensors. Please try again.")
        if msg['text'] == "/status":
            info = f'''
Here the relay status
Light: {light_control.status()}
Pump: {pump_control.status()}
Fan In: {fanIn_control.status()}
Fan Out: {fanOut_control.status()}
Fan Insiede: {fanInside_control.status()}
            '''
            bot.sendMessage(chat_id, info)
        if msg['text'] == "/getCurrentTimer":
            bot.sendMessage(chat_id, f'The light is going to turn ON at {status["startTime"]}:00 and then turn OFF at {status["endTime"]}:00')
        if '/changeStartTime' in msg['text']:
            try:
                h = int(msg['text'].split(' ')[1].strip())
                if 0 <= h < 24:
                    status["startTime"] = h
                    update_status(status)
                    bot.sendMessage(chat_id, f'The light is now going to turn ON at {h}:00')
                else:
                    bot.sendMessage(chat_id, "Incorrect data format!")
            except Exception as e:
                if DEBUG:
                    print(f"Error changing timer: {e}")
                else:
                    bot.sendMessage(chat_id, "You have not insert a valid hour number!")
        if '/changeEndTime' in msg['text']:
            try:
                h = int(msg['text'].split(' ')[1].strip())
                if 0 <= h < 24:
                    status["endTime"] = h
                    update_status(status)
                    bot.sendMessage(chat_id, f'The light is now going to turn OFF at {h}:00')
                else:
                    bot.sendMessage(chat_id, "Incorrect data format!")
            except Exception as e:
                if DEBUG:
                    print(f"Error changing timer: {e}")
                else:
                    bot.sendMessage(chat_id, "You have not insert a valid hour number!")

def main():
    MessageLoop(bot, handle).run_as_thread()
    while True:
        if status['startTime'] <= datetime.now().hours <= status['endTime']:
            light_control.turnOn()
            fanInside_control.turnOn()
        else:
            light_control.turnOff()
            fanInside_control.turnOff()
            
        try:
            hum, temp = dht.readData()
            if  temp < 20 or hum < 40:
                fanIn_control.turnOff()
                fanInside_control.turnOff()
                fanOut_control.turnOff()
                bot.sendMessage(CHAT_ID, f'Temperature or Humidity Too Hight!\nTemperature: {temp:.2f} ºC\nHumidity: {hum:.2f} %')
            if temp > 30 or hum > 70:
                fanIn_control.turnOn()
                fanInside_control.turnOn()
                fanOut_control.turnOn()
                bot.sendMessage(CHAT_ID, f'Temperature or Humidity Too Low!\nTemperature: {temp:.2f} ºC\nHumidity: {hum:.2f} %')

            if not water_level.readData():
                pump_control.turnOff()
                bot.sendMessage(CHAT_ID, "Water level is low! The water tank is empty.")

        except Exception as e:
            bot.sendMessage(CHAT_ID, f'{e}')
        sleep(60)