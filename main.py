import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


def write_csv(data):
    with open('link.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['href'],))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('table', class_='table').select('tr>td:nth-child(1)')
    for td in tds:
        link = td.find('a').get('href')
        print(link)
        data = {
            'href': link
        }
        write_csv(data)


def main():
    for page in range(1, 1063):
        url = f'https://toppub.xyz/publications?page={page}'
        get_page_data(get_html(url))


if __name__ == '__main__':
    main()
