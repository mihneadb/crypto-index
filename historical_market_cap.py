import json
import re

from bs4 import BeautifulSoup
import requests

date = '20171029'
data = []

for i in range(52):
    r = requests.get('https://coinmarketcap.com/historical/%s/#BTC' % date)
    soup = BeautifulSoup(r.text, 'html5lib')

    try:
        rows = soup.find_all('table', {'id': 'currencies-all'})[0].find_all('tr')[1:]
    except:
        continue

    week_data = []
    for row in rows:
        try:
            market_cap = float(row.find('td', {'class': 'market-cap'}).get('data-btc'))
        except ValueError:
            # Sometimes value is '?' for market cap.
            market_cap = 0

        coin_data = {
            'price': float(row.find('a', {'class': 'price'}).get('data-btc')),
            'name': row.find_all('td')[2].text,
            'volume': float(row.find('a', {'class': 'volume'}).get('data-btc')),
            'market_cap': market_cap
        }
        week_data.append(coin_data)

    data.append([date, week_data])

    # Find prev week date.
    for a in soup.find('ul', {'class': 'bottom-paginator'}).find_all('a'):
        if 'Previous Week' in a.text:
            date = re.search(r'\d+', a.get('href')).group(0)
            break
    else:
        print 'Stopped, nothing after', date
        break

with open('scrape_results.json', 'w') as f:
    json.dump(data, f)

import ipdb; ipdb.set_trace()
