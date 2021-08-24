# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import w3lib.html

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies

    def process_item(self, item, spider):

        if (spider.name == 'hhru'):
            item['salary'] = self.process_salary_hh(item['salary'])
        elif (spider.name == 'sjru'):
            item['salary'] = self.process_salary_sj(item['salary'])

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, salary):
        salary_min = None
        salary_max = None
        salary_currency = None

        salary_list = salary.replace(u'\xa0', '').split()

        salary_currency = salary_list[-1]
        if (len(salary_list) == 4):
            salary_min = int(salary_list[0])
            salary_max = int(salary_list[2])
        elif (salary_list[0] == 'от'):
            salary_min = int(salary_list[1])
        elif (salary_list[0] == 'до'):
            salary_max = int(salary_list[1])

        if ((salary_min is None) and (salary_max is None)):
            salary_currency = None

        return (salary_min, salary_max, salary_currency)

    def process_salary_sj(self, salary):
        salary_min = None
        salary_max = None
        salary_currency = None

        salary = w3lib.html.remove_tags(salary)
        salary_list = salary.replace(u'\xa0', ' ').split()

        salary_currency = salary_list[-1]
        if (len(salary_list) == 6):
            salary_min = int(salary_list[0] + salary_list[1])
            salary_max = int(salary_list[3] + salary_list[4])
        elif (salary_list[0] == 'от'):
            salary_min = int(salary_list[1] + salary_list[2])
        elif (salary_list[0] == 'до'):
            salary_max = int(salary_list[1] + salary_list[2])

        if ((salary_min is None) and (salary_max is None)):
            salary_currency = None

        return (salary_min, salary_max, salary_currency)
        #return salary