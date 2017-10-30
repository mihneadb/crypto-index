import unittest

from bittrex.bittrex import Bittrex, API_V1_1
from mock import patch

from constants import MAIN_CURRENCY
from market_bittrex import get_market_data, get_balance


class TestMarketBittrex(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.get_bittrex_patcher = patch('market_bittrex.get_bittrex')
        cls.mock_get_bittrex = cls.get_bittrex_patcher.start()
        cls.mock_get_bittrex.return_value = Bittrex(None, None, api_version=API_V1_1)

    @classmethod
    def tearDownClass(cls):
        cls.get_bittrex_patcher.stop()

    @patch('bittrex.bittrex.Bittrex.get_market_summaries')
    def test_get_market_data(self, mock_summaries):
        mock_summaries.return_value = {
            u'message': u'',
            u'result': [
                {u'Ask': 0.0390995,
                 u'BaseVolume': 540.79017391,
                 u'Bid': 0.03900011,
                 u'Created': u'2016-10-28T17:13:10.833',
                 u'High': 0.04,
                 u'Last': 0.0390001,
                 u'Low': 0.0368343,
                 u'MarketName': u'BTC-ZEC',
                 u'OpenBuyOrders': 1012,
                 u'OpenSellOrders': 11702,
                 u'PrevDay': 0.039174,
                 u'TimeStamp': u'2017-10-30T18:42:36.54',
                 u'Volume': 14111.93199843},
                {u'Ask': 0.0032211,
                 u'BaseVolume': 292.91330531,
                 u'Bid': 0.00321995,
                 u'Created': u'2017-06-05T16:39:49.07',
                 u'High': 0.003468,
                 u'Last': 0.00322,
                 u'Low': 0.0028577,
                 u'MarketName': u'BTC-ZEN',
                 u'OpenBuyOrders': 1446,
                 u'OpenSellOrders': 3735,
                 u'PrevDay': 0.00317999,
                 u'TimeStamp': u'2017-10-30T18:42:19.29',
                 u'Volume': 94613.73704344}
            ],
            u'success': True
        }

        market_data = get_market_data(MAIN_CURRENCY)
        expected_market_data = [
            {'name': 'ZEC', 'volume': 14111.93199843, 'price': (0.0390995 + 0.03900011) / 2},
            {'name': 'ZEN', 'volume': 94613.73704344, 'price': (0.0032211 + 0.00321995) / 2},
        ]
        self.assertEqual(market_data, expected_market_data)

    @patch('bittrex.bittrex.Bittrex.get_balances')
    def test_get_balance(self, mock_balances):
        mock_balances.return_value = {
            u'message': u'',
            u'result': [
                {'Currency': 'BTC',
                 'Balance': 15.0,
                 'Available': 10.0,
                 'Pending': 0.0,
                 'CryptoAddress': None}
            ],
            u'success': True
        }

        balance = get_balance()
        expected_balance = [
            {'name': 'BTC', 'value': 10}
        ]
        self.assertEqual(balance, expected_balance)
