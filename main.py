#!/usr/bin/env python3

import json
from datetime import datetime, timedelta
from threading import Timer
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

def update_status(status_data):
    try:
        with open('src/resources/status.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(status_data))
    except Exception as e:
        raise ValueError(f"Error updating status: {str(e)}")

def buildDate(hours, minutes):
    now = datetime.now()
    try:
        new_datetime = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=int(hours),
            minute=int(minutes),
            second=0,
            microsecond=0
        )
        if new_datetime < datetime.now():
            new_datetime += timedelta(days=1)

        return new_datetime
    except:
        return now    

def init():
    global status, timer_time, bot, light_control, dht, soil_moisture, pump_control, fanOut_control, fanIn_control, water_level, fanInside_control, co2_sensor
    with open('src/resources/status.json', 'r', encoding='utf-8') as f:
        status = json.load(f)
    hm = status["startTime"].split(":")
    timer_time = buildDate(hm[0], hm[1])
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
    global timer_time
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    if content_type == 'text':
        if msg['text'] == "/start":
            welcome = '''Welcome farmer to the highest tech growbox
/start --> print welcome messagge
/sensors --> print growbox sensors's infos
/status --> print relay status
/getCurrentTimer --> print when the light will turn on
/changeCurrentTimer --> change the time when the light will turn on
/vegetative --> change to vegetative mode
/flowering --> change to vegetative mode 
            '''
            bot.sendMessage(chat_id, welcome)
        if msg['text'] == "/sensors":
            try:
                hum, temp = dht.readData()
                soil_moi = soil_moisture.readData()
                info = f'''
{"Vegetative" if status["vegetative"] else "Flowering"}
Temperature: {temp:.2f} ºC
Humidity: {hum:.2f} %
Soil Moisture: {soil_moi}
                '''
                bot.sendMessage(chat_id, info)
            except Exception as e:
                bot.sendMessage(chat_id, e)
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
            bot.sendMessage(chat_id, f'The light is going to turn ON at {timer_time.strftime("%H:%M")}')
        if '/changeCurrentTimer' in msg['text']:
            try:
                hm = msg['text'].split(' ')[1].split(':')
                if len(hm) == 2:
                    hours, minutes = map(int, hm)
                    if 0 <= hours < 24 and 0 <= minutes < 60:
                        status["startTime"] = ':'.join(hm)
                        update_status(status)
                        timer_time = buildDate(hours, minutes)
                        bot.sendMessage(chat_id, f'The light is now going to turn ON at {timer_time.strftime("%H:%M")}')
                    else:
                        bot.sendMessage(chat_id, "Invalid time format!")
                else:
                    bot.sendMessage(chat_id, "Incorrect data format!")
            except Exception as e:
                bot.sendMessage(chat_id, f"Error: {e}")
        if msg['text'] == "/vegetative":
            status["vegetative"] = 0
            update_status(status)
            bot.sendMessage(chat_id, f'Set to vegetative mode')
        if msg['text'] == "/flowering":
            status["vegetative"] = 1
            update_status(status)
            bot.sendMessage(chat_id, f'Set to flowering mode')

def main():
    init()

    global timer_time
    MessageLoop(bot, handle).run_as_thread()
    while True:
        if datetime.now() > timer_time:
            if status["vegetative"] == 0 and light_control.status() == 0:
                light_control.turnOn()
                fanInside_control.turnOn()
                timer_time += timedelta(hours=status["lightHours"]["vegetativeON"])
            if status["vegetative"] == 0 and light_control.status() == 1:
                light_control.turnOff()
                fanInside_control.turnOff()
                timer_time += timedelta(hours=status["lightHours"]["vegetativeOFF"])
            if status["vegetative"] == 1 and light_control.status() == 0:
                light_control.turnOn()
                fanInside_control.turnOn()
                timer_time += timedelta(hours=status["lightHours"]["flowering"])
            if status["vegetative"] == 1 and light_control.status() == 1:
                light_control.turnOff()
                fanInside_control.turnOff()
                timer_time += timedelta(hours=status["lightHours"]["flowering"])

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