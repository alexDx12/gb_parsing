# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class ProductparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.db_leroymerlin

    def features_description(self, item):
        return dict(zip(item['feature_names'], item['feature_values']))

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        item['features'] = self.features_description(item)
        del item['feature_names']
        del item['feature_values']
        if not collection.find_one({"_id": item['_id']}):
            collection.insert_one(item)
        return item

class ProductPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'{item["_id"]}/{item["url"].split("/")[-2]}.jpg'