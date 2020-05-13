# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeroyparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.geek

    def process_item(self, item, spider):
        item['price'] =int(item['price'].replace(' ', ''))
        item['spec'] = self.spec_transform(item['spec'][:])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def spec_transform(self, specs:list):
        result = dict()
        for i in range(0, len(specs), 2):
            result[specs[i]] = specs[i+1]
        return result


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None):
        file_name = request.url.split('/')[-1]
        art = file_name[:-4].split('_')[0]
        return art + '/' + file_name

