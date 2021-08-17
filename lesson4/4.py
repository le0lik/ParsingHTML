import requests
from pprint import pprint
from pymongo import MongoClient
from lxml import html

client = MongoClient('127.0.0.1', 27017)
db = client['news']
coll = db.lenta

base_url = 'https://lenta.ru'

headers = {
#    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4183.2 Safari/537.36'
    'User-Agent': 'Chrome/99.0.4183.2 Safari/537.36'
}

response = requests.get(base_url, headers=headers)
dom = html.fromstring(response.text)
blocks = dom.xpath("//a/time[@class='g-time']/..")

for i in blocks:
    block = {}
    block['source'] = base_url
    block['title'] = i.xpath("./text()")[0].replace('\xa0', ' ')
    block['url'] = base_url + i.xpath("./@href")[0]
    block['date'] = i.xpath("./time/@title")[0]

    #pprint(block)
    coll.update_one({'url': block['url']}, {'$set': block}, upsert=True)

