# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.geek

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['salary'] = self.get_salary_hh(item['salary'][:])

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def get_salary_hh(self, salary:list):
        result = [None, None, None]
        if len(salary) == 1:
            return result
        if 'от ' in salary:
            result[0] = int(salary[salary.index('от ') + 1].replace(chr(160), ''))
        if ' до ' in salary:
            result[1] = int(salary[salary.index(' до ') + 1].replace(chr(160), ''))
        if 'от ' not in salary or ' до ' not in salary:
            result[2] = salary[3]
        else:
            result[2] = salary[5]
        return  result
