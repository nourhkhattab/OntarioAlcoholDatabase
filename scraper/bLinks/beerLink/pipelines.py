# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from db.oadb import OADB

class LinkPipeline(object):

    def __init__(self):
        self.db = OADB()

    def open_spider(self, spider):
        self.db.startBeerLinks()

    def close_spider(self, spider):
        self.db.endBeerLinks()
        self.db.close()

    def process_item(self, item, spider):
        self.db.addBeerLink(item['link'])
        return item

