"""Вариант II

Написать программу, которая собирает товары «В тренде» с сайта техники 
mvideo и складывает данные в БД. Сайт можно выбрать и свой. Главный критерий 
выбора: динамически загружаемые товары.
"""

# Импорт внешних библиотек и скриптов
from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint
from pymongo import MongoClient

# Подключение базы данных
client = MongoClient('localhost', 27017)
db = client["news_db"]

# Подготовка страницы к сбору данных
driver = webdriver.Chrome(executable_path='/Users/alexander/Documents/GeekBrains/II_четверть/Методы_сбора_и_обработки_данных_из_сети_Интернет/repository/lesson_5/chromedriver')
driver.maximize_window()
driver.implicitly_wait(10)
driver.get('https://www.mvideo.ru/')
driver.execute_script("window.scrollTo(0, 1500)")
button = driver.find_element(By.XPATH, "//span[contains(text(), 'В тренде')]")
button.click()

# Сбор данных со страницы в базу данных
product_cards_group = driver.find_element(By.XPATH, "//mvid-product-cards-group")
product_names = product_cards_group.find_elements(By.CLASS_NAME, "product-mini-card__name")
product_prices = product_cards_group.find_elements(By.CLASS_NAME, "price__main-value")
products = zip(product_names, product_prices)

for product in products:
    product_data = {}
    product_name = product[0].text
    product_link= product[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
    product_price = int(product[1].text.replace(' ', ''))
    product_data["product name"] = product_name
    product_data["product link"] = product_link
    product_data["product price"] = product_price
    pprint(product_data)
    if not db.mvideo_collection.find_one({"product link": product_link}):
        db.mvideo_collection.insert_one(product_data) 

# Завершение работы
driver.quit()
