import requests
from pprint import pprint
#import json
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient


def insertVacancy(db_collection, vac):
    db_collection.update_one({'link': vac['link']}, {'$set': vac}, upsert=True)

def serachVacancyBySalary(db_collection, salary):
    return list(db_collection.find(
        {'$or': ({'salary_min': {'$gt': salary}},
                 {'salary_max': {'$gt': salary}})
        }
    ))

def parseBlock(block):
    title = block.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()
    link = block.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']

    salary_block = block.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    salary_text = None if salary_block is None else salary_block.getText().replace(u'\u202f', '')
    salary_min = None
    salary_max = None
    salary_currency = None

    if salary_text is not None:
        salary_list = salary_text.split()

        salary_currency = salary_list[-1]
        if (len(salary_list) == 4):
            salary_min = int(salary_list[0])
            salary_max = int(salary_list[2])
        elif (salary_list[0] == 'от'):
            salary_min = int(salary_list[1])
        elif (salary_list[0] == 'до'):
            salary_max = int(salary_list[1])

    return {
        'title': title,
        'link': link,
        'salary_min': salary_min,
        'salary_max': salary_max,
        'salary_currency': salary_currency
    }

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
coll = db.hh

vacancies = []

base_url = 'https://hh.ru'
init_url = base_url + '/search/vacancy'

headers = {
#    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4183.2 Safari/537.36'
    'User-Agent': 'Chrome/99.0.4183.2 Safari/537.36'
}

params = {
    'area': '2',
    'fromSearchLine': 'true',
    'st': 'searchVacancy',
    'text': 'python',
    'items_on_page': 20
}

next_url = init_url

while next_url:
    print(next_url)

    response = requests.get(next_url, headers=headers, params=params)
    soup = bs(response.text, 'html.parser')

    for block in soup.find_all('div', {'class': 'vacancy-serp-item'}):
        #vacancies.append(parseBlock(block))
        insertVacancy(coll, parseBlock(block))

    next_item = soup.find('a', {'data-qa': 'pager-next'})
    next_url = None if next_item is None else base_url + next_item.get('href')
    params = None

#with open('file.json', 'w') as out_file:
#    json.dump(vacancies, out_file)

searchSalary = int(input('Please enter minimum Salary: '))
pprint(serachVacancyBySalary(coll, searchSalary))
