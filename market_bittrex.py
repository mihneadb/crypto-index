import json

from bittrex.bittrex import Bittrex, API_V1_1


def get_bittrex():
    with open('key.json') as f:
        data = json.load(f)
        return Bittrex(data['key'], data['secret'], api_version=API_V1_1)


def get_market_data(currency):
    summaries = get_bittrex().get_market_summaries()
    relevant_summaries = [i for i in summaries['result'] if i['MarketName'].startswith(currency)]
    return [get_market_data_entry(s, currency) for s in relevant_summaries]


def get_market_data_entry(summary, currency):
    """Converts from Bittrex format to our own."""
    return {
        'name': summary['MarketName'].replace('%s-' % currency, ''),
        'volume': summary['Volume'],
        # Hope for the best.
        'price': (summary['Ask'] + summary['Bid']) / 2,
    }


def get_balance():
    balances = get_bittrex().get_balances()
    return [get_balance_entry(b) for b in balances['result']]


def get_balance_entry(balance):
    return {
        'name': balance['Currency'],
        'value': balance['Available'],
    }
