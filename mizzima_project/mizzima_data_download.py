import requests
from bs4 import BeautifulSoup
from urllib.request import urljoin
import csv
proxies = {
  'https': '186.34.32.89:53281'
}
def download_pager_link(url):
    print("Starting requests", url, "========================================================")
    req = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(req.text, "html.parser")
    pager_link = []
    pager = soup.find('ul', class_='pager')
    page_url = ""
    if pager is not None:
        links = pager.find_all('a', href=True)
        last_link = links[len(links) - 1]
        link = urljoin(target_url, last_link.get('href'))
        print(link)
        arr = str(link).split('=')
        no_of_page = int(arr[len(arr) - 1])
        print("The number of pager for ", no_of_page)
        for j in range(no_of_page + 1):
            for i in range(len(arr) - 1):
                page_url += arr[i]
            page_url += '='
            page_url += str(j)
            pager_link.append(page_url)
            page_url = ""

    else:
        print("No page more ")
    print("Finish ", url, "==========================================================")
    return pager_link


target_url = 'http://www.mizzimaburmese.com/'
nav_title = []
nav_link = []
crawedlink = []
crawedtitle = []
crawednewslink = []
crawednewstitle = []
filename = 'F:\mizzimasavecsv\mizzima_navigation_link.csv'
with open(filename, mode='r', encoding='utf-8') as mizzimadataread:
    csv_reader = csv.reader(mizzimadataread, delimiter=',')
    for row in csv_reader:
        temp_title = ""
        for r in row:
            if not target_url in r:
                temp_title = r
            else:
                nav_title.append(temp_title)
                nav_link.append(r)
filename = 'F:\mizzimasavecsv\mizzimacrawedlink.csv'
with open(filename, mode='r', encoding='utf-8') as mizzimadataread:
    csv_reader = csv.reader(mizzimadataread, delimiter=',')
    for row in csv_reader:
        temp_title = ""
        for r in row:
            if not target_url in r:
                temp_title = r
            else:
                crawedtitle.append(temp_title)
                crawedlink.append(r)
filename = 'F:\mizzimasavecsv\mizzimacrawednewslink.csv'
with open(filename, mode='r', encoding='utf-8') as mizzimadataread:
    csv_reader = csv.reader(mizzimadataread, delimiter=',')
    for row in csv_reader:
        temp_title = ""
        for r in row:
            if not target_url in r:
                temp_title = r
            else:
                crawednewstitle.append(temp_title)
                crawednewslink.append(r)
news_main_title = []
for k in range(len(nav_title)):
    news_main_link = nav_link[k]
    link_arr = str(news_main_link).split('/')
    if(len(link_arr[len(link_arr)-1])<30):
        if link_arr[len(link_arr)-1] not in news_main_title:
            news_main_title.append(link_arr[len(link_arr)-1])
        else:
            news_main_title.append(link_arr[len(link_arr) - 1]+ str(link_arr[len(link_arr) - 2]))
    else:
        news_main_title.append(nav_title[k])
def download_real_news_links(url_link,y):
    real_news = []
    req = requests.get(url_link, proxies=proxies)
    soup = BeautifulSoup(req.text, 'html.parser')
    news_div = soup.find('div', id_='content')
    try:
        a = news_div.find_all('a', href=True)
    except Exception:
        a = soup.findAll('a', href=True)
    for link in a:
        temp_link = urljoin(target_url, link.get('href'))
        link_arr = str(temp_link).split('/')
        if link_arr[len(link_arr) - 1].isdigit():
            real_news.append(temp_link)
    real_news = set(real_news)
    for news_link in real_news:
        if news_link not in crawednewslink:
            print("Starting download$$$$", news_link)
            req = requests.get(news_link, proxies=proxies)
            soup = BeautifulSoup(req.text, "html.parser")
            news_title = ""
            try:
                title = soup.find('div', class_='news-details-title')
                news_title = title.text
            except Exception:
                news_title = ""
            author_name = ""
            try:
                author = soup.find('div', class_='news-details-author-by')
                author_name = author.text
            except Exception:
                author_name = ""
            div = soup.find('div', class_='news-details-info')
            date = ""
            try:
                div_date = div.find('div', class_='news-details-date')
                date_div = div_date.find('span', class_='date-display-single')
                date = date_div.text
            except Exception:
                date = ""
            news_type = soup.find('div', class_='news-details-info')
            news_detail = ""
            try:
                a = news_type.find_all('a', href=True)
                for links in a:
                    for link in links:
                        news_detail += link
            except Exception:
                news_detail = ""
            paragraph = soup.find('div', class_='field-item even')
            paragraph_text = ""
            if paragraph is not None:
                for p in paragraph.findChildren():
                    if p.name == 'div':
                        p.clear()
                paragraph_text = paragraph.text
            else:
                paragraph_text = ""
            filename = 'F:\mizzimasavecsv\mizzima_' + news_main_title[y] + '.csv'
            print(filename)
            with open(filename, mode='a', encoding='utf-8') as mizzimadata:
                mizzimadatabase = csv.writer(mizzimadata, delimiter=',', quotechar='"',
                                             quoting=csv.QUOTE_ALL)
                mizzimadatabase.writerow(
                    [str(news_title), str(author_name), str(date), str(paragraph_text), news_detail])
                print("Saving successful ", news_title, author_name)

            filename = 'F:\mizzimasavecsv\mizzimacrawednewslink.csv'
            with open(filename, mode='a', encoding='utf-8') as mizzimadata:
                mizzimadatabase = csv.writer(mizzimadata, delimiter=',', quotechar='"',
                                             quoting=csv.QUOTE_ALL)
                mizzimadatabase.writerow(
                    [str(news_title), str(news_link)])
                print("Saving successful ", news_title, news_link)
            news_detail = ""
            crawednewslink.append(news_link)
            crawednewstitle.append(news_title)
            news_detail = ""
        else:
            print("link is already crawled")
    real_news = []
    filename = 'F:\mizzimasavecsv\mizzimacrawedlink.csv'
    print(filename)
    with open(filename, mode='a', encoding='utf-8') as mizzimadata:
        print("Download Start")
        mizzimadatabase = csv.writer(mizzimadata, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        mizzimadatabase.writerow([news_main_title[y], url_link])
        print("Saving successful ", news_main_title[y], url_link)
        print("Download finish")
    crawedlink.append(news_main_title[y])


y = 0
# Starting request url from navigation
for url in nav_link:
    print(url, "======")
    if url not in crawedlink:
        pager_url_link = download_pager_link(url)
        if len(pager_url_link) != 0:
            for url_link in pager_url_link:
                download_real_news_links(url_link, y)
        else:
            print("No page found")
            download_real_news_links(url, y)
    else:
        print("This url is already crawled")
    filename = 'F:\mizzimasavecsv\mizzimacrawedlink.csv'
    print(filename)
    with open(filename, mode='a', encoding='utf-8') as mizzimadata:
        print("Download Start")
        mizzimadatabase = csv.writer(mizzimadata, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        mizzimadatabase.writerow([news_main_title[y], url])
        print("Saving successful ", news_main_title[y], url)
        print("Download finish")
    crawedlink.append(news_main_title[y])
    y += 1
