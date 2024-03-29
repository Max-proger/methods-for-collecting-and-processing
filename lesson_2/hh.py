import requests
from bs4 import BeautifulSoup
import pandas as pd


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
url = 'https://hh.ru'
params = {'area': '1',
          'items_on_page': '20',
          'text': 'Python',
          'search_period': '30',
          'page': '0'}

last_page = 100

vacancies = []

for page in range(0, last_page + 1):
    params['page'] = str(page)
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies_list = dom.find_all('div', {'class': 'vacancy-serp-item'})

    for vacancy in vacancies_list:
        vacancies_data = {}
        vacansy_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText().replace(u'\xa0', u' ')
        vacansy_link = vacancy.find('a', {'data-qa': "vacancy-serp__vacancy-title"}).get('href')

        try:
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText().replace(
                '\u202f', '').replace('–', '').split()
        except:
            salary = None
        if not salary:
            salary_min = None
            salary_max = None
            currency_of_salary = None
        elif salary[0] == 'от':
            salary_min = int(salary[1])
            salary_max = None
            currency_of_salary = salary[2]
        elif salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1])
            currency_of_salary = salary[2]
        else:
            salary_min = int(salary[0])
            salary_max = int(salary[1])
            currency_of_salary = salary[2]

        vacancies_data['name'] = vacansy_name
        vacancies_data['link'] = vacansy_link
        vacancies_data['salary_min'] = salary_min
        vacancies_data['salary_max'] = salary_max
        vacancies_data['currency_of_salary'] = currency_of_salary
        vacancies_data['site_name'] = 'hh.ru'
        vacancies.append(vacancies_data)

df = pd.DataFrame(vacancies)
df.to_csv('hh.csv', encoding="utf-8-sig")

