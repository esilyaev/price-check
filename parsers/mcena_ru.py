import json
from configs.app_config import Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def get_data(url: str, refresh: bool) -> dict:
    POS_NAME = 'Арматура А500С ГОСТ Р 52544'
    CATEGORY_ID = '247116597'  # see in table category
    UNIT = 'тонна'

    if refresh:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        # options.add_argument('--log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        browser = webdriver.Chrome(Config.GetChromeDriverPath(),
                                   options=options)

        browser.get(url)

        with open(file='mcena.html', mode='w') as out_file:
            out_file.write(browser.page_source)

    with open(file='mcena.html', mode='r') as html_file:
        src = html_file.read()

    soup = BeautifulSoup(src, 'lxml')

    price_table = soup.find('table', id='prices-table')
    table_header = price_table.find_all('tr')[0]
    vendors_links = table_header.find_all('th', class_='prices__vendor')
    final_list = []
    vendors = []
    for v in vendors_links:
        info = v.find('div', class_='prices-vendor')\
                .find('div', class_='prices-vendor__header').find('a')
        vendors.append({
            'store': ' '.join(info.text.split()),
            'url': info.get('href')
        })

    prices = price_table.find('tbody').find_all('tr')
    for p in prices:
        items = p.find_all('td')
        for i in range(len(vendors)):
            try:
                price = int(''.join(items[3 + i].text.split(' ')))
            except:
                price = None

            final_list.append({
                'name': POS_NAME + ' ' + items[0].find('a', class_='prices__article-link').text,
                'price': price,
                'unit': UNIT,
                'store': vendors[i]['store'],
                'category_id': CATEGORY_ID
            })

    return final_list


def main(refresh=False):
    url = 'https://www.mcena.ru/metalloprokat/armatura/a500s-gost-r-52544_ceny'
    data = get_data(url, refresh=refresh)

    return data


if __name__ == '__main__':
    main()
