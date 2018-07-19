# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from scrapy.conf import settings
import pymongo
import time


class LagouPipeline(object):
    def __init__(self):
        # self.file = codecs.open("ladou.json", "w", encoding="utf-8")
        self.num = 0
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']

        client = pymongo.MongoClient(host=host, port=port)

        mdb = client[dbname]
        self.post = mdb[settings['MONGODB_SHEETNAME']]

    def process_item(self, item, spider):
        # content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        # self.file.write(content)
        data = dict(item)
        self.post.insert(data)
        time.sleep(2)
        self.num += 1
        print self.num
        return item

    # def close_spider(self, spider):
    #    self.file.close()
