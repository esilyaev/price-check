#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def get_data(url, refresh=False):

    STORE = url.split('/')[2]
    CATEGORY_ID = '247116597'  # see in table category
    UNIT = 'тонна'

    if refresh:
        headers = {
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
        }
        # r = requests.get(url, headers=headers)
        # with open(file=f"{url.split('/')[2]}.html", mode='w') as file:
        #     file.write(r.text)

        # with open(file=f"{url.split('/')[2]}.html", mode='r') as file:
        #     src = file.read()

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--log-level=3')

        browser = webdriver.Chrome(
            'Lib/driver/chromedriver.exe', options=options)

        browser.get(url)

        time.sleep(10)
        browser.find_element(by=webdriver.common.by.By.CSS_SELECTOR,
                             value='#region_id_1 > img').click()

        time.sleep(5)

        with open(file=f"{url.split('/')[2]}.html", mode='w', encoding='utf-8') as file:
            file.write(browser.page_source)

        browser.close()
        browser.quit()

    with open(file=f"{url.split('/')[2]}.html", mode='r', encoding='utf-8') as file:
        src = file.read()
    final_list = []

    soup = BeautifulSoup(src, 'html.parser')
    table = soup.find(
        'table', class_='standart-table w100').find('tbody')

    table_rows = table.find_all('tr')

    for row in table_rows:
        tds = row.find_all('td')

        meta = tds[0].text + tds[1].text + tds[2].text
        name = ''.join(meta.split())

        price = int(''.join(tds[-1].text.split("\xa0")))

        final_list.append({
            'name': meta,
            'price': price,
            'unit': UNIT,
            'store': STORE,
            'category_id': CATEGORY_ID
        })

    return final_list


def main(refresh=False):
    url = 'https://www.agrupp.com/pricelist/?sub_group=11202'

    data = get_data(url=url, refresh=refresh)
    return data


if __name__ == '__main__':
    main()
