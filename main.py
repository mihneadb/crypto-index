from constants import MAIN_CURRENCY, ValueKeys
from index import get_sell_rebalance_orders, get_buy_rebalance_orders
from market_bittrex import get_balance, get_market_data


if __name__ == '__main__':
    TOP_LIMIT = 10
    VALUE_KEY = ValueKeys.MARKET_CAP

    balance = get_balance()
    market_data = get_market_data(MAIN_CURRENCY)

    sell_orders = get_sell_rebalance_orders(market_data, balance, top_limit=TOP_LIMIT, value_key=VALUE_KEY)
    buy_orders = get_buy_rebalance_orders(market_data, balance, top_limit=TOP_LIMIT, value_key=VALUE_KEY)

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
