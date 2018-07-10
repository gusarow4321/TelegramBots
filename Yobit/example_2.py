# coding: utf-8

import requests
from from_yobit import get_btc_eth
from time import sleep

token = '<token>'
url = 'https://api.telegram.org/bot' + token + '/'
global last_update
last_update = 0


def get_updates():
    upd = url + 'getupdates'
    r = requests.get(upd)
    return r.json()


def get_message():
    data = get_updates()
    last = data['result'][-1]

    upd_id = last['update_id']

    global last_update

    if last_update != upd_id:
        last_update = upd_id
        chat_id = last['message']['chat']['id']
        text_mes = last['message']['text']
        return {'chat_id': chat_id, 'text': text_mes}
    return None


def send_message(chat_id, text='Wait a second, please...'):
    mes = url + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(mes)


def send_price(chat_id):
    price = get_btc_eth()
    text = 'BTC price: {} usd\nETH price: {} usd'.format(round(float(price[0]), 2), round(float(price[1]), 2))
    res = url + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(res)


while True:
    message = get_message()
    if message is not None:
        if message['text'] == '/price':
            send_price(message['chat_id'])
        else:
            send_message(message['chat_id'], "I don't understand")
    sleep(3)
