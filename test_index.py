import unittest

from constants import Actions, ValueKeys
from index import Index
from order_spec import OrderSpec


class TestIndex(unittest.TestCase):
    def test_get_rebalance_orders(self):
        market_data = [
            {'name': 'VRT', 'volume': 9000, 'price': 0.1},
            {'name': 'ETH', 'volume': 10000, 'price': 0.3},
            {'name': 'FOO', 'volume': 42, 'price': 42},
        ]
        global_market_data = [
            {'name': 'VRT', 'volume': 9000, 'market_cap': 9000, 'price': 0.1},
            {'name': 'ETH', 'volume': 10000, 'market_cap': 10000, 'price': 0.3},
            {'name': 'FOO', 'volume': 42, 'market_cap': 42, 'price': 42},
        ]

        balance = [
            {'name': 'BTC', 'value': 1.3},
            {'name': 'VRT', 'value': 5.2},
            {'name': 'ETH', 'value': 7},
        ]

        orders = Index().get_rebalance_orders(market_data, global_market_data, balance,
                                              top_limit=2, value_key=ValueKeys.MARKET_CAP)[0]
        expected_orders = [
            OrderSpec(action=Actions.SELL,
                      coin='ETH',
                      price=0.3,
                      amount=0.4666666666666668),
            OrderSpec(action=Actions.BUY,
                      coin='VRT',
                      price=0.1,
                      amount=14.399999999999999)
        ]

        self.assertEqual(orders, expected_orders)

    def test_get_rebalance_orders_sell_entire_coin(self):
        # This includes a coin in portfolio that we need to entirely get rid off.
        market_data = [
            {'name': 'VRT', 'volume': 9000, 'price': 0.1},
            {'name': 'ETH', 'volume': 10000, 'price': 0.3},
            {'name': 'FOO', 'volume': 42, 'price': 42},
            {'name': 'TOSELL', 'volume': 42, 'price': 1},
        ]
        global_market_data = [
            {'name': 'VRT', 'volume': 9000, 'market_cap': 9000, 'price': 0.1},
            {'name': 'ETH', 'volume': 10000, 'market_cap': 10000, 'price': 0.3},
            {'name': 'FOO', 'volume': 42, 'market_cap': 42, 'price': 42},
            {'name': 'TOSELL', 'volume': 42, 'market_cap': 42, 'price': 1},
        ]

        balance = [
            {'name': 'BTC', 'value': 1.0},
            {'name': 'VRT', 'value': 5.2},
            {'name': 'ETH', 'value': 7},
            {'name': 'TOSELL', 'value': 0.3},
        ]

        orders = Index().get_rebalance_orders(market_data, global_market_data, balance, top_limit=2)[0]
        expected_orders = [
            OrderSpec(action=Actions.SELL,
                      coin='ETH',
                      price=0.3,
                      amount=0.4666666666666668),
            OrderSpec(action=Actions.SELL,
                      coin='TOSELL',
                      price=1,
                      amount=0.3),
            OrderSpec(action=Actions.BUY,
                      coin='VRT',
                      price=0.1,
                      amount=14.399999999999999),
        ]

        self.assertEqual(orders, expected_orders)

    def test_get_top_assets(self):
        market_data = [
            # ETH is missing, assuming the exchange does not sell it.
            {'name': 'FOO', 'volume': 42, 'price': 42},
            {'name': 'VRT', 'volume': 9000, 'price': 0.1},
        ]
        global_market_data = [
            {'name': 'VRT', 'volume': 9000, 'market_cap': 9000, 'price': 0.1},
            {'name': 'ETH', 'volume': 10000, 'market_cap': 10000, 'price': 0.3},
            {'name': 'FOO', 'volume': 42, 'market_cap': 42, 'price': 42},
        ]

        top_assets = Index().get_top_assets(market_data, global_market_data,
                                            value_key=ValueKeys.MARKET_CAP,
                                            top_limit=2)
        expected_top_assets = ['VRT', 'FOO']
        self.assertEqual(top_assets, expected_top_assets)

    def test_get_top_market_data(self):
        market_data = [
            # ETH is missing, assuming the exchange does not sell it.
            {'name': 'FOO', 'volume': 42, 'price': 42},
            {'name': 'VRT', 'volume': 9000, 'price': 0.1},
        ]
        global_market_data = [
            {'name': 'VRT', 'volume': 9000, 'market_cap': 9000, 'price': 0.1},
            {'name': 'ETH', 'volume': 10000, 'market_cap': 10000, 'price': 0.3},
            {'name': 'FOO', 'volume': 42, 'market_cap': 42, 'price': 42},
        ]

        top_market_data = Index().get_top_market_data(market_data, ['VRT', 'FOO'])
        expected_top_market_data = [
            {'name': 'VRT', 'volume': 9000, 'price': 0.1},
            {'name': 'FOO', 'volume': 42, 'price': 42},
        ]
        self.assertEqual(top_market_data, expected_top_market_data)
