# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy0712

    def process_item(self, item, spider):

        if spider.name == 'hhru':
            item['min'], item['max'], item['cur'], item['tax'] = self.hhru_process_salary(item['salary'])

        if spider.name == 'superjobru':
            item['min'], item['max'], item['cur'], item['tax'] = self.superjobru_process_salary(item['salary'])

        del item['salary']

        collection = self.mongobase[spider.name]
        if not collection.find_one({"link": item['link']}):
            collection.insert_one(item)

        return item

    def hhru_process_salary(self, salary):

        min = None
        max = None
        cur = None
        tax = None

        if salary[0] == 'от ':
            min = int(salary[1].replace(u'\xa0', u''))

        if salary[0] == 'до ':
            max = int(salary[1].replace(u'\xa0', u''))

        if salary[0] != 'з/п не указана':
            cur = salary[-2]
            tax = salary[-1]
            if salary[2] == ' до ':
                max = int(salary[3].replace(u'\xa0', u''))

        return min, max, cur, tax

    def superjobru_process_salary(self, salary):

        min = None
        max = None
        cur = None
        tax = None

        if salary[0] == 'от':
            val = salary[2].split()
            if len(val) == 3:
                min = int(val[0] + val[1])
                cur = val[2]

        if len(salary) > 4:
            min = salary[0].replace(u'\xa0', u'')
            max = salary[4].replace(u'\xa0', u'')
            cur = salary[6]

        if salary[0] == 'до':
            val = salary[2].split()
            if len(val) == 3:
                max = int(val[0] + val[1])
                cur = val[2]

        return min, max, cur, tax




