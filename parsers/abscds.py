#!/usr/bin/python3
# -*- coding: utf-8 -*-


from selenium import webdriver
from configs.app_config import Config
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json


def get_data(url, refresh=False):

    STORE = url.split('/')[2]
    CATEGORY_ID = '17286'  # see in table category
    UNIT = 'м3'

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
        # options.add_argument('--log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        browser = webdriver.Chrome(
            Config.GetChromeDriverPath(), options=options)

        browser.get(url)

        time.sleep(10)
        browser.find_element(by=webdriver.common.by.By.CSS_SELECTOR,
                             value='#section-content > div.moto-widget.moto-widget-container.moto-container_content_55e95316 > div.moto-widget.moto-widget-row.row-fixed > div > div > div.moto-cell.col-sm-3 > div > div > ul > li:nth-child(1) > p > a').click()

        time.sleep(5)

        with open(file=f"{url.split('/')[2]}.html", mode='w', encoding='utf-8') as file:
            file.write(browser.page_source)

        browser.close()
        browser.quit()

    with open(file=f"{url.split('/')[2]}.html", mode='r', encoding='utf-8') as file:
        src = file.read()
    final_list = []

    soup = BeautifulSoup(src, 'html.parser')

    table = soup.find('table')

    trs = table.find_all('tr')[2:11]

    for tr in trs:
        td = tr.find_all('td')
        if len(td) == 6:
            td = td[1:]
        pos_name = ' '.join(td[0].text.split())
        pos_price = int(td[4].text)

        final_list.append({
            'name': pos_name,
            'price': pos_price,
            'unit': UNIT,
            'store': STORE,
            'category_id': CATEGORY_ID
        })

    # with open('test.json', mode='w', encoding="utf-8") as out_file:
    #     json.dump(final_list, out_file, indent=4, ensure_ascii=False)

    return final_list


def main(refresh=True):
    url = 'https://abscds.ru/products/'

    data = get_data(url=url, refresh=refresh)
    return data


if __name__ == '__main__':
    main()
