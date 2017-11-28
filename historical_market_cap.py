import json
import re

from bs4 import BeautifulSoup
import requests

from coinmarketcap import scrape_coins

date = '20171126'
data = []


for i in range(52):
    r = requests.get('https://coinmarketcap.com/historical/%s/#BTC' % date)
    soup = BeautifulSoup(r.text, 'html5lib')

    week_data = scrape_coins(soup)

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
