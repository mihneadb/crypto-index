MAIN_CURRENCY = 'BTC'
PRECISION_DECIMALS = 8
MIN_DIFF = 10 ** (PRECISION_DECIMALS - 1)
TOP_LIMIT = 20
# What to choose the best coins by. (volume or market_cap)
# market_cap seems better lately.
VALUE_KEY = 'market_cap'

class Actions(object):
    SELL = 'sell'
    BUY = 'buy'
