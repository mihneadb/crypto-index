import json

from binance.client import Client

from constants import MAIN_CURRENCY, Actions


def get_binance():
    with open('binance_key.json') as f:
        data = json.load(f)
        return Client(data['key'], data['secret'])


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
    b = get_binance()
    symbol = '%s%s' % (order_spec.coin, MAIN_CURRENCY)

    if order_spec.action == Actions.BUY:
        fn = b.order_limit_buy
    elif order_spec.action == Actions.SELL:
        fn = b.order_limit_sell
    else:
        raise ValueError("Invalid action")

    return fn(symbol=symbol, quantity=order_spec.amount, price=str(order_spec.price))
