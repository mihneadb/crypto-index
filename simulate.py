import json

from index import get_rebalance_orders, get_portfolio_value


INITIAL_BTC = 1
balance = [
    {'name': 'BTC', 'value': INITIAL_BTC},
]

def portfolio_to_balance(portfolio):
    b = []
    for key, value in portfolio.items():
        b.append({'name': key, 'value': value})
    return b


if __name__ == '__main__':
    with open('scrape_results.json') as f:
        historical_data = json.load(f)

    # Sort by week asc.
    historical_data.sort(key=lambda x: x[0])

    for week, market_data in historical_data[-8:]:
        orders, portfolio = get_rebalance_orders(market_data, balance, top_limit=300)
        balance = portfolio_to_balance(portfolio)

    prices = {item['name']: item['price'] for item in market_data}
    total_value = get_portfolio_value(balance, prices)
    # print portfolio
    # print len(portfolio)
    print "Started with %f BTC, ended with (equivalent) %f BTC." % (INITIAL_BTC, total_value)
