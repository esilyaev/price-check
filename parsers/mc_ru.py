#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def get_data(url: str, refresh=False) -> list:

    STORE = url.split('/')[2]
    CATEGORY_ID = '247116597'  # see in table category
    UNIT = 'тонна'

    if refresh:
        headers = {
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
        }
        r = requests.get(url, headers=headers)
        with open(file=f"{url.split('/')[2]}.html", mode='w', encoding="utf-8") as file:
            file.write(r.text)

    final_list = []

    with open(file=f"{url.split('/')[2]}.html", mode='r', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'html.parser')
    table = soup.find(
        'table', class_='catalogTable').find('tbody')

    table_rows = table.find_all('tr')

    for row in table_rows:
        meta = row.find('meta', {
            'itemprop': 'name'
        })['content']

        price = row.find('td', {
            'data-price-val': '1'
        })

        try:
            price = int(''.join(price.text.split()))
        except:
            price = None

        final_list.append({
            'name': meta,
            'price': price,
            'unit': UNIT,
            'store': STORE,
            'category_id': CATEGORY_ID
        })

    return final_list


def main(refresh=False):
    url = 'https://mc.ru/metalloprokat/armatura_riflenaya_a3/mark/a500s'

    data = get_data(url=url, refresh=refresh)
    return data


if __name__ == '__main__':
    main()
