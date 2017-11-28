MAIN_CURRENCY = 'BTC'
PRECISION_DECIMALS = 2
MIN_DIFF = 0.1 ** (PRECISION_DECIMALS - 1)
TOP_LIMIT = 20


class Actions(object):
    SELL = 'sell'
    BUY = 'buy'


# What to choose the best coins by. (volume or market_cap)
# market_cap seems better lately.
class ValueKeys(object):
    MARKET_CAP = 'market_cap'
    VOLUME = 'volume'
