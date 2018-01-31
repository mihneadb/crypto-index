import json

from binance.client import Client
import ccxt

from constants import MAIN_CURRENCY, Actions
from helpers import truncate


def get_binance():
    with open('binance_key.json') as f:
        data = json.load(f)
        return Client(data['key'], data['secret'])


def get_binance_ccxt():
    with open('binance_key.json') as f:
        data = json.load(f)
        return ccxt.binance({'apiKey': data['key'], 'secret': data['secret']})


def get_balance():
    account = get_binance().get_account()
    formatted = [get_balance_entry(b) for b in account['balances']]
    return [b for b in formatted if b['value']]


def get_balance_entry(balance):
    return {
        'name': balance['asset'],
        'value': float(balance['free']),
    }


def exec_order_spec(order_spec):
    b = get_binance_ccxt()

    symbol = '%s/%s' % (order_spec.coin, MAIN_CURRENCY)
    if order_spec.action == Actions.BUY:
        fn = b.create_limit_buy_order
    elif order_spec.action == Actions.SELL:
        fn = b.create_limit_sell_order
    else:
        raise ValueError("Invalid action")

    return fn(symbol, order_spec.amount, order_spec.price)

    # symbol = '%s%s' % (order_spec.coin, MAIN_CURRENCY)
    #
    # if order_spec.action == Actions.BUY:
    #     fn = b.order_limit_buy
    # elif order_spec.action == Actions.SELL:
    #     fn = b.order_limit_sell
    # else:
    #     raise ValueError("Invalid action")
    #
    # return fn(symbol=symbol, quantity=truncate(order_spec.amount, 3), price='%f' % order_spec.price)