import requests
import json
from secret import password


user = input('Введите пользователя: ')
link = f'https://api.github.com/users/{user}/repos'
username = 'denis-volkov'
params = {}
headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.3.332 (beta) Yowser/2.5 Safari/537.36'}
r = requests.get(link, auth=(username, password), headers=headers)

answer = json.loads(r.text)
print(f'У пользователя {user} есть репозитории в количестве {len(answer)}')
for i in answer:
    print('{} {}.'.format(i['name'].ljust(20), i['url']))


# Яндекс Погода
# API_Key = 'cc06e44b-3d3a-44e7-b49e-f88d67c4354b'
# link = 'https://api.weather.yandex.ru/v1/forecast'
# mailru_towers = (55.796749, 37.537371)
# headers = {'X-Yandex-API-Key': API_Key}
#
# r = requests.get(link+'?lat={}&lon={}&lang={}'.format(mailru_towers[0], mailru_towers[1], 'ru_RU'), headers=headers)
#
# answer = json.loads(r.text)
# print('Температура рядом с офисом GeekBrains {} градуса, ощущается как {}'.format(answer['fact']['temp'], answer['fact']['feels_like']))
