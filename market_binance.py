import json
import os
import sys

from binance.client import Client
import ccxt

from constants import MAIN_CURRENCY, Actions
from helpers import truncate


def get_binance():
    path = os.path.join(sys.path[0], 'binance_key.json')
    with open(path) as f:
        data = json.load(f)
        return Client(data['key'], data['secret'])


def get_binance_ccxt():
    path = os.path.join(sys.path[0], 'binance_key.json')
    with open(path) as f:
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


def get_market_data():
    tickers = get_binance().get_all_tickers()
    market_data = []
    for ticker in tickers:
        symbol = ticker['symbol']
        
        if not symbol.endswith(MAIN_CURRENCY):
            continue

        market_data.append({
            'name': symbol.split(MAIN_CURRENCY)[0],
            'price': float(ticker['price']),
            'volume': 1,
            'market_cap': 1
        })

    # Add btc as well.
    btc = {'name': 'BTC', 'price': 1}
    market_data.append(btc)

    return market_data


def exec_order_spec(order_spec):
    b = get_binance_ccxt()

    symbol = '%s/%s' % (order_spec.coin, MAIN_CURRENCY)
    if order_spec.action == Actions.BUY:
        # fn = b.create_limit_buy_order
        fn = b.create_market_buy_order
    elif order_spec.action == Actions.SELL:
        # fn = b.create_limit_sell_order
        fn = b.create_market_sell_order
    else:
        raise ValueError("Invalid action")

    # return fn(symbol, order_spec.amount, order_spec.price)
    return fn(symbol, order_spec.amount)

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
