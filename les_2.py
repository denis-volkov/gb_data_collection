import requests
from bs4 import BeautifulSoup as bs
import re

link_base = 'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text='
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 OPR/67.0.3575.137'}

job = input('Введите должность: ').strip().split()
job = '+'.join(job)
result = []

page = 0
while True:
    link = link_base + job +'&page=' + str(page)
    req = requests.get(link, headers=headers).text
    html = bs(req, 'lxml')

    block_vacancy = html.findAll('div', {'class': 'vacancy-serp-item'})
    for i in block_vacancy:
        data = i.find('a', {'class': 'bloko-link HH-LinkModifier'})
        vacancy = {'name': data.text}
        vacancy['ref'] = re.search('(?<=href=")[a-zA-Z0-9:\/.?=%]+', str(data)).group()
        vacancy['site'] = 'Head hunter'
        data = i.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not data:
            vacancy['zp'] = [None, None, None]
        else:
            data = str(data.text)
            vacancy['zp'] = [None, None, re.search('[a-zA-Zа-яА-Я.]+$', data).group()]
            data = data[:-len(vacancy['zp'][2])]
            data = data.replace(' ', '').replace(chr(160), '')
            if 'от' in data:
                vacancy['zp'][0] = re.search('\d+', data).group()
            elif 'до' in data:
                vacancy['zp'][1] = re.search('\d+', data).group()
            else:
                vacancy['zp'][0] = data.split('-')[0]
                vacancy['zp'][1] = data.split('-')[1]
        result.append(vacancy)
    if not html.findAll('a', {'class': 'HH-Pager-Controls-Next'}):
        break
    page += 1

for i in result:
    print('Вакансия:', i['name'])
    print('Зарплата от:', i['zp'][0])
    print('Зарплата до:', i['zp'][1])
    print('Валюта:', i['zp'][2])
    print('Ссылка:', i['ref'])
    print('Взято с сайта:', i['site'])
    print()
