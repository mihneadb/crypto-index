from collections import namedtuple

from binance.client import Client
from scipy import stats

from constants import MAIN_CURRENCY, TOP_LIMIT, ValueKeys, NUM_DAYS_TO_CHECK
from index import Index
from market_binance import get_binance


Kline = namedtuple('Kline', [
    'open_time',
    'open',
    'high',
    'low',
    'close',
    'volume',
    'close_time',
    'quote_asset_volume',
    'number_of_trades',
    'buy_base_asset_volume',
    'buy_quote_asset_volume',
    'ignore'
])


class BinanceGrowthIndex(Index):
    def get_top_assets(self, exchange_market_data, global_market_data,
                       value_key=ValueKeys.MARKET_CAP, top_limit=TOP_LIMIT):
        klines = get_all_klines()
        top_assets = get_best_growth_assets(klines, top_limit)
        return top_assets


def get_all_klines():
    client = get_binance()
    exchange_info = client.get_exchange_info()
    symbols = [s for s in exchange_info['symbols'] if s['quoteAsset'] == MAIN_CURRENCY]

    klines = {}
    for s in symbols:
        historical_klines = client.get_historical_klines(s['symbol'],
                                                         Client.KLINE_INTERVAL_1DAY,
                                                         '%s days ago UTC' % NUM_DAYS_TO_CHECK,
                                                         'now UTC')
        klines[s['baseAsset']] = historical_klines
    return klines


def get_best_growth_assets(klines, max_count=10):
    """
    Computes the slope of the growing assets and returns the best.
    :param klines:
    :return: List of assets (strings), sorted desc by slope.
    """

    # Drop ones that are not growing.
    growing_klines = {}
    for asset, historical_klines in klines.iteritems():
        values = [float(Kline(*h).close) for h in historical_klines]

        # If not growing.
        if sorted(values) != values:
            continue

        growing_klines[asset] = historical_klines

    slopes = []
    for asset, historical_klines in growing_klines.iteritems():
        ys = [float(Kline(*h).close) for h in historical_klines]
        xs = range(len(ys))
        slope, _, _, _, _ = stats.linregress(xs, ys)
        slopes.append((asset, slope))

    slopes.sort(key=lambda p: p[1], reverse=True)
    return [p[0] for p in slopes][:max_count]


def klines_to_market_data(klines):
    market_data = []

    for asset, historical_klines in klines.iteritems():
        entry = {
            'name': asset,
            # Hope for the best.
            'price': float(Kline(*historical_klines[-1]).close),
            # Just for compatibility.
            ValueKeys.MARKET_CAP: 1,
            ValueKeys.VOLUME: 1,
        }
        market_data.append(entry)

    return market_data
