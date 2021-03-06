import requests
from bs4 import BeautifulSoup
import csv
import threading

lock = threading.Lock()


def write(url):
    with open('link_new.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(url)


def get_html(url):
    r = requests.get(url)
    if r.status_code < 299 and r.status_code > 199:
        return r.text
    else:
        write(url)
        return ""


def write_csv(data):
    lock.acquire()
    with open('data.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(data)
    lock.release()


def validate_button(all_tag):
    if all_tag[0].select('a')[0].text == 'Read publication':
        return None
    else:
        return all_tag[0].select('a')[0].text


def get_page_data(url):
    html = get_html(url)
    if html == "":
        return
    soup = BeautifulSoup(html, 'lxml')
    first_column = soup.find('div', class_='media')
    two_column = soup.find('div', class_='card-stats text-lg-right')

    title = None
    try:
        title = first_column.find('h2', class_='mb-0').text
    except:
        pass
        # print(url)
    all_tag = first_column.find('div', class_='media-body').select('div', class_='pb-4')
    all_tags = all_tag[0].select('a')

    img = ''
    description = ''
    button = first_column.find('div', class_='mt-3').select('a')
    read_publication = button[0].get('href')
    twitter = None
    facebook = None
    try:
        description = first_column.find('div', class_='media-body').find('p').text
    except:
        print('')
    for a in button:
        if a.find('i', class_='fa-facebook') is not None:
            facebook = a.get('href')
        if a.find('i', class_='fa-twitter') is not None:
            twitter = a.get('href')
    span = two_column.find('div', class_='d-inline-block').select('span')
    followers = span[0].text.replace('\n', '').strip().replace(',', '')

    tags_1 = None
    tags_2 = None
    tags_3 = None
    tags_4 = None
    tags_5 = None
    try:
        img = first_column.find('img').get('src')
    except:
        print('None IMG')
    try:
        tags_1 = validate_button(all_tag)
        tags_2 = all_tags[1].text
        tags_3 = all_tags[2].text
        tags_4 = all_tags[3].text
        tags_5 = all_tags[4].text
    except:
        print('error')
    data = (
        description,
        url,
        title,
        tags_1,
        tags_2,
        tags_3,
        tags_4,
        tags_5,
        followers,
        read_publication,
        twitter,
        facebook,
        img,
    )
    write_csv(data)
    return 'Ok'


def main():
    t1 = Thread(0, 3000)
    t2 = Thread(3000, 6000)
    t3 = Thread(6000, 9000)
    t4 = Thread(9000, 12000)
    t5 = Thread(12000, 15927)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    threads = []
    threads.append(t1)
    threads.append(t2)
    threads.append(t3)
    threads.append(t4)
    threads.append(t5)
    for t in threads:
        t.join()
    print("_______________________END_______________________")


def anic(i, j):
    print(i, j)
    content_list = None
    lock.acquire()
    my_file = open("list_link.txt", "r")
    content_list = my_file.readlines()
    my_file.close();
    lock.release()
    while i < j:
        print(content_list[i])
        print(get_page_data(content_list[i].replace('\n', '')))
        i += 1


class Thread(threading.Thread):
    def __init__(self, i, j):
        threading.Thread.__init__(self)
        self.i = i
        self.j = j

    def run(self):
        anic(self.i, self.j)


if __name__ == '__main__':
    main()
