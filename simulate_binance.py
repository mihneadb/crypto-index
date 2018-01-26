import argparse
import json

from mock.mock import patch

from binance_growth_index import BinanceGrowthIndex, klines_to_market_data
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


def get_limited_historical_data(historical_data, step):
    limited_history = {}

    for asset in historical_data:
        data = historical_data[asset][step: 3 + step]
        if len(data) != 3:
            continue
        limited_history[asset] = data

    return limited_history


def get_market_data(historical_data, step):
    return klines_to_market_data(get_limited_historical_data(historical_data, step))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simulate BTC indexing across historical data.")
    parser.add_argument('--top-limit', dest='top_limit',
                        default=25, type=int,
                        help="Number of best coins to choose when indexing")

    args = parser.parse_args()

    with open('31klines.json') as f:
        historical_data = json.load(f)

    patcher = patch('binance_growth_index.get_all_klines')
    get_all_klines_mock = patcher.start()

    for i in range(31 - 2):
        market_data = get_market_data(historical_data, i)
        get_all_klines_mock.return_value = get_limited_historical_data(historical_data, i)
        orders, portfolio = BinanceGrowthIndex().get_rebalance_orders(market_data, market_data, balance,
                                                                      top_limit=args.top_limit)
        balance = portfolio_to_balance(portfolio)

    prices = {item['name']: item['price'] for item in market_data}
    total_value = Index().get_portfolio_value(balance, prices)
    # print portfolio
    # print len(portfolio)
    print "Started with %f BTC, ended with (equivalent) %f BTC." % (INITIAL_BTC, total_value)
