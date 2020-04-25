from lxml import html
from pprint import pprint
import requests
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36 OPR/68.0.3618.56'}

main_link = 'https://news.mail.ru'
news = []
req = requests.get(main_link, headers=headers)
page = html.fromstring(req.text)
data = page.xpath("//a[contains(@class, 'js-topnews__item')]")
# Главные новости на mail.ru с картинками
for i in data:
    link = i.xpath(".//@href")[0]
    if 'sportmail' not in link:
        link = main_link + link
    new = {'ref': link}
    new['title'] = i.xpath(".//span[contains(@class, 'js-topnews__notification')]/text()")[0].replace(chr(160), ' ')
    new['date'] = str(datetime.date.today()) # Главные новости текущей датой
    new['source'] = html.fromstring(requests.get(link, headers=headers).text).xpath(
        "//a[@class='link color_gray breadcrumbs__link']//span[@class='link__text']/text()")[0]
    news.append(new)
# Главные новости на mail.ru без картинок
data = page.xpath("//ul[@data-module]//a")
for i in data:
    link = i.xpath(".//@href")[0]
    if 'sportmail' not in link:
        link = main_link + link
    new = {'ref': link}
    new['title'] = i.xpath(".//text()")[0].replace(chr(160), ' ')
    new['date'] = str(datetime.date.today()) # Главные новости текущей датой
    new['source'] = html.fromstring(requests.get(link, headers=headers).text).xpath(
        "//a[@class='link color_gray breadcrumbs__link']//span[@class='link__text']/text()")[0]
    news.append(new)


pprint(news)

