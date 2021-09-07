import os
import datetime

from coinmarketcap import get_coinmarketcap
from constants import MAIN_CURRENCY, ValueKeys, Actions
from index import Index
from market_binance import get_balance, get_market_data, exec_order_spec


if __name__ == '__main__':
    noinput = os.getenv('NOINPUT', False)
    TOP_LIMIT = 50
    VALUE_KEY = ValueKeys.MARKET_CAP

    balance = get_balance()
    market_data = get_market_data()
    global_market_data = get_coinmarketcap(MAIN_CURRENCY)

    orders, ideal_portfolio = Index().get_rebalance_orders(market_data, global_market_data,
                                                           balance,
                                                           top_limit=TOP_LIMIT, value_key=VALUE_KEY)
    sell_orders = [o for o in orders if o.action == Actions.SELL]
    buy_orders = [o for o in orders if o.action == Actions.BUY]

    from pprint import pprint
    print("Now:", datetime.datetime.now())

    print("Balance now:")
    pprint(balance)

    print("Ideal portfolio:")
    pprint(ideal_portfolio)

    print("To sell:")
    pprint(sell_orders)

    print("To buy:")
    pprint(buy_orders)

    if noinput:
        r = 'Y'
    else:
        print("Exec sells?")
        r = input("Y/n ")
    if r == 'Y':
        for order in sell_orders:
            print(">>", order)
            try:
                pprint(exec_order_spec(order))
            except Exception as e:
                print("\n\n ERROR \n\n", e, "\n\n")

    if noinput:
        r = 'Y'
    else:
        print("Exec buys?")
        r = input("Y/n ")
    if r == 'Y':
        for order in buy_orders:
            print(">>", order)
            try:
                pprint(exec_order_spec(order))
            except Exception as e:
                print("\n\n ERROR \n\n", e, "\n\n")

    print("<<<<<<<<<<<<<<<<<<< DONE >>>>>>>>>>>>>>>>>>")
