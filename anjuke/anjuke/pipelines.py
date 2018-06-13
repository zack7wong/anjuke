# -*- coding: utf-8 -*-
import hashlib
import time
import pymongo
from twisted.enterprise import adbapi
import re
import pymysql
from anjuke.spiders.zufang import ZufangSpider

#
# from pymongo import MongoClient
#
# client = MongoClient()
# collection = client['zufang']['anjuke']
#
# class AnjukePipeline(object):
#
#     def process_item(self, item, spider):
#         print(111,item)
#         item["_id"] = hashlib.md5(item['beautify']+item["house_position"]).hexdigest()
#         print(item["_id"])
#         collection.insert(dict(item))
#         print("save ok")
#         return item

class AnjukePipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABSE', 'items')
        )


    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        print('>>>>', item)
        print('\n')
        item["crawl_time"] = str(time.strftime("%Y-%m-%d %X", time.localtime()))
        city_abbreviate = re.findall('[a-zA-Z]+', item['start_url'])[1]
        
        try:
            self.db[city_abbreviate].insert(item)
        except Exception as e:
            print(e)
        print('save ok \n')
        return item
