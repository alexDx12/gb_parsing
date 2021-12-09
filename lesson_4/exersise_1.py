"""Написать приложение, которое собирает основные новости с сайта на выбор 
news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. 
Структура данных должна содержать:
    - название источника;
    - наименование новости;
    - ссылку на новость;
    - дата публикации.
    Сложить собранные новости в БД

Минимум один сайт, максимум - все три.
"""

# Импорт внешних библиотек и скриптов
from lxml import html
import requests
from pymongo import MongoClient

# Подключение базы данных
client = MongoClient('localhost', 27017)
db = client["news_db"]

# Формирование параметров запросов с сайта https://lenta.ru/
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36'}
response = requests.get('https://lenta.ru/', headers=header)
dom = html.fromstring(response.text)
items = dom.xpath("//section[contains(@class, 'b-top7-for-main')]/*/div[contains(@class, 'item')]/a | //h2/a")

temp = []
# Скраппинг новостей
for item in items:
    news = {}
    source_link = 'https://lenta.ru/'
    name = ''.join(item.xpath("./text()")).replace(u'\xa0', u' ')
    news_link = 'https://lenta.ru' + ''.join(item.xpath("./@href"))
    date = ''.join(item.xpath("./time/@title"))
    news['source link'] = source_link
    news['name'] = name
    news['news link'] = news_link
    news['date'] = date
    if name and not db.lenta_collection.find_one({'news link': news_link}):
        db.lenta_collection.insert_one(news)  
    # if name - фильтрация тэга с изображением первой новости, 
    # not db.lenta_collection.find_one({'news link': news_link}) - проверка отсутствия текущей новости в базе данных.