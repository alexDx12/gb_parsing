"""Вариант I

Написать программу, которая собирает входящие письма из своего или тестового 
почтового ящика и сложить данные о письмах в базу данных (от кого, дата 
отправки, тема письма, текст письма полный).

Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172#
"""

# Импорт внешних библиотек и скриптов
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

# Подключение базы данных
client = MongoClient('localhost', 27017)
db = client["letters_db"]

# Подготовка страницы к сбору данных
driver = webdriver.Chrome(executable_path='/Users/alexander/Documents/GeekBrains/II_четверть/Методы_сбора_и_обработки_данных_из_сети_Интернет/repository/lesson_5/chromedriver')

driver.implicitly_wait(120)
driver.maximize_window()
driver.get("https://mail.ru/")
element = driver.find_element(By.XPATH, "//input[@name='login']")
element.send_keys("study.ai_172@mail.ru")
button = driver.find_element(By.XPATH, "//button[@data-testid='enter-password']")
button.click()
element = driver.find_element(By.XPATH, "//input[@name='password']")
element.send_keys("NextPassword172#")
button = driver.find_element(By.XPATH, "//button[@data-testid='login-to-mail']")
button.click()

# Сбор ссылок на письма
links = set()
stop_element = 0
while True:
    
    elements = driver.find_elements(By.XPATH, "//a[@data-id]")
    last_element = elements[-1]
    
    # условие выхода из цикла при получении последнего элемента письма на странице:
    if last_element == stop_element:
        break
    
    for element in elements:
        link = element.get_attribute("href")
        links.add(link)
    
    stop_element = last_element
    
    actions = ActionChains(driver)
    actions.move_to_element(last_element).perform()

#  Извлечение данных из писем и отправка их в базу данных
for link in links:
    letter = {}
    driver.get(link)
    author = driver.find_element(By.XPATH, "//div[@class='letter__author']/span[@class='letter-contact']").text
    date = driver.find_element(By.XPATH, "//div[@class='letter__author']/div[@class='letter__date']").text
    topic = driver.find_element(By.XPATH, "//h2[@class='thread__subject']").text
    body = driver.find_element(By.XPATH, "//div[@class='letter__body']").text
    letter["author"] = author
    letter["date"] = date
    letter["topic"] = topic
    letter["body"] = body
    letter["link"] = link
    if not db.mail_ru_collection.find_one({"link": link}):
        db.mail_ru_collection.insert_one(letter)
        
# Завершение работы
driver.quit()