import json
import os
import sys

import requests
from bs4 import BeautifulSoup

from constants import MAIN_CURRENCY


def get_coinmarketcap(main_currency=MAIN_CURRENCY):
    path = os.path.join(sys.path[0], 'coinmarketcap_key.json')
    with open(path) as f:
        data = json.load(f)
        key = data['key']

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': key
    }
    params = {
        'limit': 200,
        'convert': 'BTC'
    }
    r = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest', params=params, headers=headers)

    return [{
        'name': c['symbol'],
        'price': c['quote']['BTC']['price'],
        'volume': c['quote']['BTC']['volume_24h'],
        'market_cap': c['quote']['BTC']['market_cap']
    } for c in r.json()['data']]

def scrape_coins(soup, main_currency=MAIN_CURRENCY, skip_main_currency=False):
    rows = soup.find_all('table', {'id': 'currencies-all'})[0].find_all('tr')[1:]

    data = []
    for row in rows:
        try:
            market_cap = float(row.find('td', {'class': 'market-cap'}).get('data-btc'))
        except ValueError:
            # Sometimes value is '?' for market cap.
            market_cap = 0

        try:
            coin_data = {
                'price': float(row.find('a', {'class': 'price'}).get('data-btc')),
                'name': row.find_all('td')[2].text,
                'volume': float(row.find('a', {'class': 'volume'}).get('data-btc')),
                'market_cap': market_cap
            }
        except ValueError:
            # Some coins have missing fields.
            continue

        # Skip main currency, can't "buy" it.
        if skip_main_currency and coin_data['name'] == main_currency:
            continue

        data.append(coin_data)

    return data
