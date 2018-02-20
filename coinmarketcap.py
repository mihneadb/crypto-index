import requests
from bs4 import BeautifulSoup

from constants import MAIN_CURRENCY


def get_coinmarketcap(main_currency=MAIN_CURRENCY):
    r = requests.get('https://coinmarketcap.com/all/views/all/')
    soup = BeautifulSoup(r.text, 'html5lib')
    return scrape_coins(soup, main_currency=main_currency)


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
