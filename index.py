from constants import MAIN_CURRENCY, MIN_DIFF, Actions
from order_spec import OrderSpec


def get_portfolio_value(balance, prices):
    """Computes total amount that the portfolio is worth."""
    portfolio_value = 0.0

    for item in balance:
        if item['name'] == MAIN_CURRENCY:
            portfolio_value += item['value']
        else:
            portfolio_value += item['value'] * prices[item['name']]

    return portfolio_value


def get_ideal_portfolio(portfolio_value, market_data):
    """Computes the equal-weighted portfolio consisting of market_data items."""
    ideal_portfolio = {}

    # We expect market_data to be filtered to the coins we care about.
    value_each = portfolio_value / len(market_data)

    for item in market_data:
        ideal_portfolio[item['name']] = value_each / item['price']

    return ideal_portfolio


def get_rebalance_orders(market_data, balance, top_limit=20):
    """Generates the required orders to rebalance the portfolio against market data.

    Orders are sorted - the sells come first.
    """
    prices = {item['name']: item['price'] for item in market_data}
    portfolio = {item['name']: item['value'] for item in balance}
    # Drop main currency from portfolio, we're not considering it here.
    portfolio.pop(MAIN_CURRENCY, None)

    top_market_data = sorted(market_data, key=lambda md: md['volume'], reverse=True)[:top_limit]
    portfolio_value = get_portfolio_value(balance, prices)
    ideal_portfolio = get_ideal_portfolio(portfolio_value, top_market_data)

    # Compute orders to exec.
    orders = []
    for coin, ideal_value in ideal_portfolio.items():
        current_value = portfolio.pop(coin, 0)
        diff = ideal_value - current_value

        # Not worth making an order for this.
        if abs(diff) < MIN_DIFF:
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
                          price=prices[coin],
                          amount=current_value)
        orders.append(order)

    # SELL < BUY so they get to the beginning of the array.
    return sorted(orders, key=lambda o: 1 if o.action == Actions.SELL else 2)