import urllib
import sys
from bs4 import BeautifulSoup
from bs4 import element
import requests
import re
from collections import defaultdict


DEPARTMENT_PATTERN = re.compile(r'\d{1,2}\.\s+(.+)\s*')
INFO_EMAIL_PATTERN = re.compile(r'([aА-ЯҐЄІЇа-яїєі\s,\.-]+)\.?\s+([a-z_@\.]+)')


response = requests.get('''http://socrates.vsau.org/wiki/index.php/Список_адрес_електронних_поштових_скринь_структурних_підрозділів_університету''')  # get-запрос

soup = BeautifulSoup(response.text, 'html.parser')

div = soup.find('div', id='mw-content-text')

res = defaultdict(list)

for elem in div:
    if isinstance(elem, element.Tag):
        if elem.span:
            search_result = re.search(DEPARTMENT_PATTERN, elem.span.text)
            if search_result:
                department = search_result.group(1).strip()
        else:
            search_result = re.search(INFO_EMAIL_PATTERN, elem.text)
            if search_result:
                res[department].append(
                    (
                        search_result.group(1).strip(),
                        search_result.group(2).strip(),
                    )
                )

for key in res:
    print(key)
    for elem in res[key]:
        print('\t', elem)









