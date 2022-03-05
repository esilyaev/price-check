import requests
from bs4 import BeautifulSoup


def get_data(url: str, refresh=False):

    if refresh:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }

        responce = requests.get(url=url, headers=headers)
        # print(responce)
        with open(file=f"{url.split('/')[2]}.html", mode='w') as file:
            file.write(responce.text)

    with open(file=f"{url.split('/')[2]}.html", mode='r', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    table = soup.find('table', class_='table_cont table_prod')\
        .find('tbody')
    table_rows = table.find_all('tr')[1:]

    final_array = []
    for tr in table_rows:
        td = tr.find_all('td')
        pos_name = ' '.join(td[0].text.split()[:-1])[:-1]
        pos_price = ''.join(td[3].text.strip().split()[:-1])

        try:
            price = int(''.join(pos_price.split()))
        except:
            price = None

        final_array.append({
            'name': pos_name,
            'price': price,
        })

    return final_array


def main(refresh=False):
    data = get_data(
        url='https://mkm-metal.ru/catalog/sort/armatura/armatura-a-500/', refresh=refresh)
    return data


if __name__ == '__main__':
    main()
