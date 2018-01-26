MAIN_CURRENCY = 'BTC'
PRECISION_DECIMALS = 8
MIN_TRADE_VALUE = 0.001  # 100.000 Satoshi (Bittrex)
TOP_LIMIT = 20
# For Binance growth.
NUM_DAYS_TO_CHECK = 2


IGNORED_CURRENCIES = ['DOGE']


class Actions(object):
    SELL = 'sell'
    BUY = 'buy'


# What to choose the best coins by. (volume or market_cap)
# market_cap seems better lately.
class ValueKeys(object):
    MARKET_CAP = 'market_cap'
    VOLUME = 'volume'
