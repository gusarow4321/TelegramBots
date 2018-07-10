# coding: utf-8

import requests


def get_btc_eth():
    r = requests.get('https://api.exmo.com/v1/ticker/').json()
    return [r['BTC_USD']['buy_price'], r['ETH_USD']['buy_price']]

