from constants import PRECISION_DECIMALS
from helpers import truncate


class OrderSpec(object):
    def __init__(self, action, coin, price, amount):
        self.action = action
        self.coin = coin
        self.price = price
        self.amount = truncate(amount, PRECISION_DECIMALS)

    def __repr__(self):
        return 'Order: %s %f of %s for %f each' % (self.action, self.amount,
                                                   self.coin, self.price)

    def __eq__(self, other):
        return (self.action == other.action and
                self.coin == other.coin and
                self.price == other.price and
                self.amount == other.amount)
