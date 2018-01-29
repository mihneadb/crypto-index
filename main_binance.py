from binance_growth_index import get_all_klines, klines_to_market_data
from constants import Actions
from index import Index
from market_binance import get_balance, exec_order_spec


if __name__ == '__main__':
    TOP_LIMIT = 20

    balance = get_balance()

    all_klines = get_all_klines()
    market_data = klines_to_market_data(all_klines)

    orders, ideal_portfolio = Index().get_rebalance_orders(market_data, market_data,
                                                           balance,
                                                           top_limit=TOP_LIMIT,
                                                           min_trade_value=0.002)
    sell_orders = [o for o in orders if o.action == Actions.SELL]
    buy_orders = [o for o in orders if o.action == Actions.BUY]

    from pprint import pprint
    print "Balance now:"
    pprint(balance)

    print "Ideal portfolio:"
    pprint(ideal_portfolio)

    print "To sell:"
    pprint(sell_orders)

    print "To buy:"
    pprint(buy_orders)

    print "Exec sells?"
    r = raw_input("Y/n ")
    if r == 'Y':
        for order in sell_orders:
            pprint(exec_order_spec(order))

    print "Exec buys?"
    r = raw_input("Y/n ")
    if r == 'Y':
        for order in buy_orders:
            pprint(exec_order_spec(order))
