import json
import requests


username = input('Введите имя пользователя github:')
url = f'https://api.github.com/users/{username}/repos'
repos = requests.get(url)
j_data = repos.json()

for repo in j_data:
    with open('repo_urls.txt', 'a+') as file:
        file.writelines(f'{repo["html_url"]}\n')

with open('github_repo.json', "w") as file:
    json.dump(j_data, file, indent=2)
