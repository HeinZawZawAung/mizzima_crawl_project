import csv
import re
import requests
from urllib.request import urljoin
from bs4 import BeautifulSoup
from urllib.request import urljoin
import time
date = time.strftime("%x").split('/')
today = ""
i = 0
for d in date:
    today += d
    if(i < len(date)-1):
        today += "-"
        i += 1


target_url = 'http://www.mizzimaburmese.com/'
req = requests.get(target_url)
soup = BeautifulSoup(req.text, "html.parser")
a = soup.findAll('a', href = True)
for link in a:
    linktemp = urljoin(target_url, link.get('href'))
    linktitle_temp = link.text
    print(linktitle_temp, "=======>", linktemp)
    print("\n\n")
    print("Start Download link====.")
    filename = 'F:\mizzimasavecsv\mainpagelink' + today + '.csv'
    print(filename)
    with open(filename, mode='a', encoding='utf-8') as mizzimadata:
        print("Download Start")
        mizzimadatabase = csv.writer(mizzimadata, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        mizzimadatabase.writerow([linktitle_temp, linktemp])
        print("Saving successful ", linktitle_temp)
        print("Download finish")

