import argparse
import json

from constants import ValueKeys
from index import Index


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
    parser = argparse.ArgumentParser(description="Simulate BTC indexing across historical data.")
    parser.add_argument('--top-limit', dest='top_limit',
                        default=25, type=int,
                        help="Number of best coins to choose when indexing")
    parser.add_argument('--weeks-back', dest='weeks_back',
                        default=52, type=int,
                        help="Number of weeks back to simulate")
    parser.add_argument('--rebalance-period', dest='rebalance_period',
                        default=1, type=int,
                        help="How often (in weeks) to rebalance")

    args = parser.parse_args()

    with open('scrape_results.json') as f:
        historical_data = json.load(f)

    # Sort by week asc.
    historical_data.sort(key=lambda x: x[0])

    for week, market_data in historical_data[-args.weeks_back::args.rebalance_period]:
        orders, portfolio = Index().get_rebalance_orders(market_data, market_data, balance,
                                                         top_limit=args.top_limit, value_key=ValueKeys.MARKET_CAP)
        balance = portfolio_to_balance(portfolio)

    prices = {item['name']: item['price'] for item in market_data}
    total_value = Index().get_portfolio_value(balance, prices)
    # print portfolio
    # print len(portfolio)
    print "Started with %f BTC, ended with (equivalent) %f BTC." % (INITIAL_BTC, total_value)
