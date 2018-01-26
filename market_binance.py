import json

from binance.client import Client


def get_binance():
    with open('binance_key.json') as f:
        data = json.load(f)
        return Client(data['key'], data['secret'])
