from constants import MAIN_CURRENCY
from index import get_sell_rebalance_orders, get_buy_rebalance_orders
from market_bittrex import get_balance, get_market_data


if __name__ == '__main__':
    TOP_LIMIT = 300
    balance = get_balance()
    market_data = get_market_data(MAIN_CURRENCY)

    sell_orders = get_sell_rebalance_orders(market_data, balance, top_limit=TOP_LIMIT)
    buy_orders = get_buy_rebalance_orders(market_data, balance, top_limit=TOP_LIMIT)

    from pprint import pprint
    print "Balance now:"
    pprint(balance)

    print "To sell:"
    pprint(sell_orders)

    print "To buy:"
    pprint(buy_orders)

    # for order in sell_orders:
    #     exec_order_spec(order)
    #
    # for order in buy_orders:
    #     exec_order_spec(order)
