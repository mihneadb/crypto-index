from constants import MAIN_CURRENCY, Actions, TOP_LIMIT, ValueKeys, MIN_TRADE_VALUE
from order_spec import OrderSpec


def get_portfolio_value(balance, prices):
    """Computes total amount that the portfolio is worth."""
    portfolio_value = 0.0

    for item in balance:
        if item['name'] == MAIN_CURRENCY:
            portfolio_value += item['value']
        else:
            portfolio_value += item['value'] * prices.get(item['name'], 0)

    return portfolio_value


def get_top_market_data(exchange_market_data, global_market_data,
                        value_key=ValueKeys.MARKET_CAP, top_limit=TOP_LIMIT):
    """Uses global market data to choose the best coins from the exchange's market."""
    sorted_global_market_data = sorted(global_market_data, key=lambda md: md[value_key], reverse=True)
    top_market_data = []

    i = 0
    total = 0
    while total < top_limit:
        for coin_data in exchange_market_data:
            if coin_data['name'] == sorted_global_market_data[i]['name']:
                top_market_data.append(coin_data)
                total += 1
                i += 1
                break
        else:
            # This coin is not sold in the exchange, skip it.
            i += 1

    return top_market_data


def get_ideal_portfolio(portfolio_value, market_data, ):
    """Computes the equal-weighted portfolio consisting of market_data items."""
    ideal_portfolio = {}

    # We expect market_data to be filtered to the coins we care about.
    value_each = portfolio_value / len(market_data)

    for item in market_data:
        ideal_portfolio[item['name']] = value_each / item['price']

    return ideal_portfolio


def get_rebalance_orders(exchange_market_data, global_market_data,
                         balance, top_limit=TOP_LIMIT, value_key=ValueKeys.MARKET_CAP):
    """Generates the required orders to rebalance the portfolio against market data.

    Looks at global market data as source of truth - tries to stick to it.
    Orders are sorted - the sells come first.
    Returns order list as well as ideal portfolio at this point.
    """
    prices = {item['name']: item['price'] for item in exchange_market_data}
    portfolio = {item['name']: item['value'] for item in balance}
    # Drop main currency from portfolio, we're not considering it here.
    portfolio.pop(MAIN_CURRENCY, None)

    top_market_data = get_top_market_data(exchange_market_data, global_market_data,
                                          value_key=value_key, top_limit=top_limit)

    portfolio_value = get_portfolio_value(balance, prices)
    ideal_portfolio = get_ideal_portfolio(portfolio_value, top_market_data)

    # Compute orders to exec.
    orders = []
    for coin, ideal_value in ideal_portfolio.items():
        current_value = portfolio.pop(coin, 0)
        diff = ideal_value - current_value

        # The exchange imposes a minimum order.
        order_value = abs(diff) * prices[coin]
        if order_value < MIN_TRADE_VALUE:
            continue

        action = Actions.BUY if diff > 0 else Actions.SELL
        order = OrderSpec(action=action,
                          coin=coin,
                          price=prices[coin],
                          amount=abs(diff))
        orders.append(order)

    # There might be some coins left that we no longer care about.
    for coin, current_value in portfolio.items():
        order = OrderSpec(action=Actions.SELL,
                          coin=coin,
                          price=prices.get(coin, 0),
                          amount=current_value)
        orders.append(order)

    # SELL < BUY so they get to the beginning of the array.
    rebalance_orders = sorted(orders, key=lambda o: 1 if o.action == Actions.SELL else 2)
    return rebalance_orders, ideal_portfolio
