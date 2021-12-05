"""1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и 
реализовать функцию, которая будет добавлять только новые вакансии/продукты в 
вашу базу.

2. Написать функцию, которая производит поиск и выводит на экран вакансии с 
заработной платой больше введённой суммы (необходимо анализировать оба поля 
зарплаты). Для тех, кто выполнил задание с Росконтролем - напишите запрос для 
поиска продуктов с рейтингом не ниже введенного или качеством не ниже 
введенного (то есть цифра вводится одна, а запрос проверяет оба поля).
"""

# Импорт внешних библиотек и скриптов
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from pymongo import MongoClient

# Вспомогательные классы и функции
def salary_func(salary):
    """Обработка всвевозможных вариантов представления заработных плат."""

    if len(salary) == 0:
        min_salary = None
        max_salary = None
        currency = None

    elif salary[0] == 'от':
        if salary[2] == '000':
            min_salary = float(salary[1] + salary[2])
        else:
            min_salary = float(salary[1])
        max_salary = None
        currency = salary[-1]

    elif salary[0] == 'до':
        min_salary = None
        if salary[2] == '000':
            max_salary = float(salary[1] + salary[2])
        else:
            max_salary = float(salary[1])
        currency = salary[-1]

    else:
        if len(salary[1]) > 1 and len(salary[4]) > 1:
            min_salary = float(salary[0] + salary[1])
            max_salary = float(salary[3] + salary[4])
        else:
            min_salary = float(salary[0])
            max_salary = float(salary[2])

        currency = salary[-1]

    return min_salary, max_salary, currency

client = MongoClient('localhost', 27017)
db = client["vacancies_db"]

# Формирование параметров запросов с сайта https://hh.ru
url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true'
headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0'}

position = input("Введите интерисующую Вас позицию: ")
position = '&text=' + position

page_count = int(input("Введите количество анализируемых страниц сайта: "))
if page_count < 1:
    page_count = 1

target_salary = float(input("Введите интерисующую Вас сумму: "))
target_currency = input("Введите валюту интерисующей Вас суммы (USD, EUR, руб.): ")

# Скраппинг вакансий
for page in range(page_count):

    page_num = 'page=' + str(page)
    response = requests.get(url+position+'&'+page_num+'&items_on_page=20', headers=headers)  # параметр items_on_page=20 (количество вакансий на странице) позволяет обойти работу ограничивающих для парсинга скриптов
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies = dom.find_all(name='div', attrs={'class': 'vacancy-serp-item'})

    for vacancy in vacancies:
        vacancy_data = {}
        name = vacancy.find(name='a').text
        company = vacancy.find(name='a', attrs={'class': 'bloko-link bloko-link_secondary'}).text.replace(u'\xa0', u' ')
        location = vacancy.find(name='div', attrs={'class': 'bloko-text bloko-text_small bloko-text_tertiary'}).next_sibling.text.replace(u'\xa0', u' ')
        if vacancy.find(name='div', attrs={'class': 'vacancy-serp-item__sidebar'}):
            salary = (vacancy.find(name='div', attrs={'class': 'vacancy-serp-item__sidebar'}).text).split()
        else:
            salary = []
        min_salary = salary_func(salary)[0]
        max_salary = salary_func(salary)[1]
        currency = salary_func(salary)[2]
        job_link = vacancy.find(name='a').get('href')
        site_link = 'https://hh.ru/'
        vacancy_data['name'] = name
        vacancy_data['company'] = company
        vacancy_data['location'] = location
        vacancy_data['min salary'] = min_salary
        vacancy_data['max salary'] = max_salary
        vacancy_data['currency'] = currency
        vacancy_data['job link'] = job_link
        vacancy_data['site link'] = site_link
        if not list(db.hh_collection.find({'job link': job_link})):
            db.hh_collection.insert_one(vacancy_data)
    next_label = dom.find_all(name='a', attrs={'class': 'bloko-button'})[-1].text
    if next_label != 'дальше':
        print(f"Достигнут максимум в количестве стрниц сайта: {page+1} стр.")
        break

# Вывод целевых вакансий
target_vacancies = list(db.hh_collection.find({
    'currency': target_currency,
    '$or': [{"min salary": {'$gt': target_salary}}, {"max salary": {'$gt': target_salary}}]
}))
for target_vacancy in target_vacancies:
    pprint(target_vacancy)
