"""1.	Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, 
        сохранить JSON-вывод в файле *.json.
"""

import requests
import json

username = input("Введите имя пользователя: ")

url = 'https://api.github.com/users/' + username + '/repos'
response = requests.get(url)
j_data = response.json()

print("\nСписок репозиториев пользователя: \n")
for repo in j_data:
    print(repo['html_url'])

with open('exercise_1.json', 'w') as f:
    json.dump(j_data, f)


