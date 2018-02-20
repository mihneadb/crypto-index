from constants import MAIN_CURRENCY, Actions, TOP_LIMIT, ValueKeys, MIN_TRADE_VALUE, IGNORED_CURRENCIES
from order_spec import OrderSpec


class Index(object):

    def get_portfolio_value(self, balance, prices, min_trade_value):
        """Computes total amount that the portfolio is worth."""
        portfolio_value = 0.0

        for item in balance:
            if item['name'] == MAIN_CURRENCY:
                portfolio_value += item['value']
            else:
                value = item['value'] * prices.get(item['name'], 0)
                if value >= min_trade_value:
                    portfolio_value += value

        return portfolio_value

    def get_top_assets(self, exchange_market_data, global_market_data,
                       value_key=ValueKeys.MARKET_CAP, top_limit=TOP_LIMIT):
        """Uses global market data to choose the best coins from the exchange's market."""
        sorted_global_market_data = sorted(global_market_data, key=lambda md: md[value_key], reverse=True)
        top_assets = []

        i = 0
        total = 0
        while total < top_limit:
            for coin_data in exchange_market_data:
                if coin_data['name'] in IGNORED_CURRENCIES:
                    continue
                if coin_data['name'] == sorted_global_market_data[i]['name']:
                    top_assets.append(coin_data['name'])
                    total += 1
                    i += 1
                    break
            else:
                # This coin is not sold in the exchange, skip it.
                i += 1

        return top_assets

    def get_top_market_data(self, exchange_market_data, top_assets):
        """Selects market data for the given top assets"""
        top_market_data = []
        for asset in top_assets:
            for coin_data in exchange_market_data:
                if coin_data['name'] == asset:
                    top_market_data.append(coin_data)
        return top_market_data

    def get_ideal_portfolio(self, portfolio_value, market_data):
        """Computes the equal-weighted portfolio consisting of market_data items."""
        ideal_portfolio = {}

        # We expect market_data to be filtered to the coins we care about.
        value_each = portfolio_value / len(market_data)

        for item in market_data:
            ideal_portfolio[item['name']] = value_each / item['price']

        return ideal_portfolio

    def get_rebalance_orders(self, exchange_market_data, global_market_data,
                             balance, top_limit=TOP_LIMIT, value_key=ValueKeys.MARKET_CAP,
                             min_trade_value=MIN_TRADE_VALUE):
        """Generates the required orders to rebalance the portfolio against market data.

        Looks at global market data as source of truth - tries to stick to it.
        Orders are sorted - the sells come first.
        Returns order list as well as ideal portfolio at this point.
        """
        prices = {item['name']: item['price'] for item in exchange_market_data}
        portfolio = {item['name']: item['value'] for item in balance}
        # Drop main currency from portfolio, we're not considering it here.
        portfolio.pop(MAIN_CURRENCY, None)

        top_assets = self.get_top_assets(exchange_market_data, global_market_data,
                                         value_key=value_key, top_limit=top_limit)
        top_market_data = self.get_top_market_data(exchange_market_data, top_assets)

        portfolio_value = self.get_portfolio_value(balance, prices, min_trade_value)
        ideal_portfolio = self.get_ideal_portfolio(portfolio_value, top_market_data)

        # Compute orders to exec.
        orders = []
        for coin, ideal_value in ideal_portfolio.items():
            # No action needed for main currency.
            if coin == MAIN_CURRENCY:
                continue

            current_value = portfolio.pop(coin, 0)
            diff = ideal_value - current_value

            # The exchange imposes a minimum order.
            order_value = abs(diff) * prices[coin]
            if order_value < min_trade_value:
                continue

            action = Actions.BUY if diff > 0 else Actions.SELL
            order = OrderSpec(action=action,
                              coin=coin,
                              price=prices[coin],
                              amount=abs(diff))
            orders.append(order)

        # There might be some coins left that we no longer care about.
        for coin, current_value in portfolio.items():
            # The exchange imposes a minimum order.
            order_value = current_value * prices.get(coin, 0)
            if order_value < min_trade_value:
                continue
            order = OrderSpec(action=Actions.SELL,
                              coin=coin,
                              price=prices.get(coin, 0),
                              amount=current_value)
            orders.append(order)

        # SELL < BUY so they get to the beginning of the array.
        rebalance_orders = sorted(orders, key=lambda o: 1 if o.action == Actions.SELL else 2)
        return rebalance_orders, ideal_portfolio
