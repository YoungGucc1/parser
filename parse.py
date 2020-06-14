import requests
from bs4 import BeautifulSoup
import csv, time

URL = 'https://www.olx.kz/hobbi-otdyh-i-sport/sport-otdyh/velo/ust-kamenogorsk/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0', 'accept': '*/*'}
FILE = 'cars2.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='block br3 brc8 large tdnone lheight24')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
    print(pagination)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='offer-wrapper')

    cars = []
    for item in items:
        cars.append({
            'title': item.find('h3', class_='lheight22 margintop5').get_text(strip=True),
            'link': item.find('a', class_='marginright5 link linkWithHash detailsLink').get('href'),
            'price': item.find('div', class_='space inlblk rel').get_text(strip=True),
        })
    return(cars)


def save_file(items, path):
    with open(path, 'w', newline='', encoding='Windows-1251') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка', 'Цена'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price']])

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
            time.sleep(5)
        save_file(cars, FILE)
        print(f'Получено {len(cars)} товаров')
    else:
        print('Error')


parse()

