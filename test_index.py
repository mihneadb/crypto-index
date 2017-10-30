import unittest

import index
from constants import Actions
from order_spec import OrderSpec


class TestIndex(unittest.TestCase):
    def test_get_rebalance_orders(self):
        market_data = [
            {'name': 'VRT', 'volume': 9000, 'price': 0.1},
            {'name': 'ETH', 'volume': 10000, 'price': 0.3},
            {'name': 'FOO', 'volume': 42, 'price': 42},
        ]

        balance = [
            {'name': 'BTC', 'value': 1.3},
            {'name': 'VRT', 'value': 5.2},
            {'name': 'ETH', 'value': 7},
        ]

        orders = index.get_rebalance_orders(market_data, balance, top_limit=2)
        expected_orders = [
            OrderSpec(action=Actions.SELL,
                      coin='ETH',
                      price=0.3,
                      amount=0.46),
            OrderSpec(action=Actions.BUY,
                      coin='VRT',
                      price=0.1,
                      amount=14.39)
        ]

        self.assertEqual(orders, expected_orders)
