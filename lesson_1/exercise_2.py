"""2.	Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. 
Ответ сервера записать в файл."""

# Запрос фотографий с марсохода, сделанных в определённую дату, с выводом одного из фото случайным образом в браузер
import requests
import json
from pprint import pprint
from random import randint
import webbrowser

# Запрос даты
date = input("Введите дату в формате YYYY-MM-DD: ")

# Создание запроса
endpoint = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
api_key = "DEMO_KEY"
query_params = {"api_key": api_key, "earth_date": date}
response = requests.get(endpoint, params=query_params)
j_response = response.json()

# Запиь запроса в файл
with open('exercise_2.json', 'w') as f:
    json.dump(j_response, f)

# Вывод фото случайным образом в браузер
photos = response.json()['photos']
len_photos = len(photos)
photo_number = randint(0, len_photos)
webbrowser.open(photos[photo_number]['img_src'])