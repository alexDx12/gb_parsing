"""
Вариант 1
    
    Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность) с 
сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта (также вводим через
input или аргументы). Получившийся список должен содержать в себе минимум:

    Наименование вакансии.
    Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
    Ссылку на саму вакансию.
    Сайт, откуда собрана вакансия.

    По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть одинаковая для
вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.
"""

# Импорт внешних библиотек и скриптов
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

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

# Скраппинг вакансий с сайта https://hh.ru
url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true'
headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0'}

position = input("Введите интерисующую Вас позицию: ")
position = '&text=' + position

page_count = int(input("Введите количество анализируемых страниц сайта: "))
if page_count < 1:
    page_count = 1

dom = BeautifulSoup()
for page in range(page_count):
    page_num = 'page=' + str(page)
    response = requests.get(url+position+'&'+page_num, headers=headers)
    page_dom = BeautifulSoup(response.text, 'html.parser')
    next_label = page_dom.find_all(name='a', attrs={'class': 'bloko-button'})[-1].text
    if next_label != 'дальше':
        print(f"Достигнут максимум в количестве стрниц: {page} стр.")
        break
    dom.append(page_dom)

vacancies = dom.find_all(name='div', attrs={'class': 'vacancy-serp-item'})
 
vacancy_list = []
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
    vacancy_list.append(vacancy_data)

# Вывод и сохранение результатов
print(pd.DataFrame(vacancy_list))

with open('exercise_1.json', 'w') as f:
    json.dump(vacancy_list, f)