import os
import time

from binance_growth_index import get_all_klines, klines_to_market_data, BinanceGrowthIndex
from constants import Actions
from index import Index
from market_binance import get_balance, exec_order_spec, get_market_data


if __name__ == '__main__':
    TOP_LIMIT = 20
    noinput = os.getenv('NOINPUT', False)

    balance = get_balance()
    market_data = get_market_data()

    orders, ideal_portfolio = BinanceGrowthIndex().get_rebalance_orders(market_data, market_data,
                                                                        balance,
                                                                        top_limit=TOP_LIMIT,
                                                                        min_trade_value=0.002)
    sell_orders = [o for o in orders if o.action == Actions.SELL]
    buy_orders = [o for o in orders if o.action == Actions.BUY]

    from pprint import pprint
    print "Now:", time.time()

    print "Balance now:"
    pprint(balance)

    print "Ideal portfolio:"
    pprint(ideal_portfolio)

    print "To sell:"
    pprint(sell_orders)

    print "To buy:"
    pprint(buy_orders)

    if noinput:
        r = 'Y'
    else:
        print "Exec sells?"
        r = raw_input("Y/n ")
    if r == 'Y':
        for order in sell_orders:
            print ">>", order
            try:
                pprint(exec_order_spec(order))
            except Exception, e:
                print "\n\n ERROR \n\n", e, "\n\n"

    if noinput:
        r = 'Y'
    else:
        print "Exec buys?"
        r = raw_input("Y/n ")
    if r == 'Y':
        for order in buy_orders:
            print ">>", order
            try:
                pprint(exec_order_spec(order))
            except Exception, e:
                print "\n\n ERROR \n\n", e, "\n\n"

    print "<<<<<<<<<<<<<<<<<<< DONE >>>>>>>>>>>>>>>>>>"
