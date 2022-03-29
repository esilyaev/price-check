#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import requests
from bs4 import BeautifulSoup


def get_data(url: str, refresh=False) -> list:

    STORE = url.split('/')[2]
    CATEGORY_ID = '17286'  # see in table category
    UNIT = 'м3'

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

    table = soup.find_all('table')[1]

    trs = table.find('tbody').find_all('tr')

    for tr in trs:
        td = tr.find_all('td')

        pos_name = ' '.join([' '.join(s.text.split()) for s in td[:2]])
        pos_price = int(''.join(td[2].text.split()[:-1]))

        final_list.append({
            'name': pos_name,
            'price': pos_price,
            'unit': UNIT,
            'store': STORE,
            'category_id': CATEGORY_ID
        })

    with open('test.json', mode='w', encoding="utf-8") as out_file:
        json.dump(final_list, out_file, indent=4, ensure_ascii=False)

    return final_list


def main(refresh=True):
    url = 'https://atlantbeton.ru/price/'

    data = get_data(url=url, refresh=refresh)
    return data


if __name__ == '__main__':
    main()
