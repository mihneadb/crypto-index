MAIN_CURRENCY = 'BTC'
PRECISION_DECIMALS = 8
MIN_DIFF = 10 ** (PRECISION_DECIMALS - 1)
TOP_LIMIT = 20
# What to choose the best coins by.
VALUE_KEY = 'volume'

class Actions(object):
    SELL = 'sell'
    BUY = 'buy'
