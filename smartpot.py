#!/usr/bin/env python3
import json
from datetime import datetime as dt
from time import sleep
from src.sensors import *
from src.resources.cred import TOKEN, CHAT_ID

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

#################################################################################################################################à

bot = None

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

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        if '/start' in msg['text'].lower():
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Stampa dashboard', callback_data='dashboard')],
                [InlineKeyboardButton(text='Stampa valori dei sensori', callback_data='sensor_data')],
                [InlineKeyboardButton(text='Stampa stato dei dispositivi', callback_data='appliance_status')]
                #[InlineKeyboardButton(text='Stampa grafico dati', callback_data='sensor_history')],
                #[InlineKeyboardButton(text='Invia una foto', callback_data='send_photo')]
            ])
            bot.sendMessage(CHAT_ID, 'Fai la tua scelta', reply_markup=keyboard)
        else:
            bot.sendMessage(CHAT_ID, 'Opzione non valida!')
    else:
        bot.sendMessage(CHAT_ID, 'Opzione non valida!')


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    if from_id == CHAT_ID:
        if 'dashboard' in msg['text'].lower():
            txt = f'Pianta:\t{}\nUptime:\t{}\n'
            bot.answerCallbackQuery(CHAT_ID, text=txt)
        elif 'sensor_data' in msg['text']:
            txt = f'Pianta:\t{}\nUptime:\t{}\n'
            bot.answerCallbackQuery(CHAT_ID, text=txt)
        elif 'appliance_status' in msg['text']:
            txt = f'Pianta:\t{}\nUptime:\t{}\n'
            bot.answerCallbackQuery(CHAT_ID, text=txt)
        else:
            bot.answerCallbackQuery(CHAT_ID, text='Opzione non valida!')

def main():
    global bot
    bot = telepot.Bot(TOKEN)
    rele = Relay()
    wat_level_in = WaterLever(9)
    wat_level_out = WaterLever(11)
    sensors = [DHT22(7), Ds18(), LM333(8)] #CCS881()
    MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()
    while True:
        data = []
        for sen in sensors:
            data.append(sen.readData())
        #TODO upload sensor data to db for statistics
        if wat_level_out.readData() == 0:
            bot.sendMessage(CHAT_ID, 'Riempi la riserva di acqua che stà per finì!')
        checkLight(rele)
        
        sleep(20)
        
if __name__ == "__main__":
    main()