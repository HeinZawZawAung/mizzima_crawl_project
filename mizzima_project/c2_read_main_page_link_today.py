import csv
import time
import requests
from bs4 import BeautifulSoup
date = time.strftime("%x").split('/')
today = ""
i = 0
for d in date:
    today += d
    if(i < len(date)-1):
        today += "-"
        i += 1



target_url = 'http://www.mizzimaburmese.com/'
crawable_title = []
crawable_link = []
uncrawable_title = []
uncrawable_link = []
filename = 'F:\mizzimasavecsv\mainpagelink' + today + '.csv'
with open(filename, mode='r', encoding='utf-8') as mizzimadataread:
    csv_reader = csv.reader(mizzimadataread, delimiter=',')
    for row in csv_reader:
        temp_title = ""
        for r in row:
            if not target_url in r:
                temp_title = r
            else:
                crawable_link.append(r)
                crawable_title.append(temp_title)

print("Original")
print(len(crawable_link))
crawable_link = set(crawable_link)
crawable_link = sorted(crawable_link, key=len)

for link in crawable_link:
    target_url = link
    req = requests.get(target_url)
    soup = BeautifulSoup(req.text, "html.parser")
    print(soup.title.text, link)
print("Final result")
print(len(crawable_link))







