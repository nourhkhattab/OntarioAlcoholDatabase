# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from db.oadb import OADB

class LcboItemPipeline(object):

    def __init__(self):
        self.db = OADB()

    def close_spider(self, spider):
        self.db.endItems()
        self.db.close()

    def process_item(self, item, spider):
        self.db.addLCBOItem(
            item['ID'],
            item['link'],
            item['name'],
            item['price'],
            item['amount'],
            item['vol'],
            item['form'],
            item['alc'],
            item['Type'],
            item['cat1'] if 'cat1' in item else "N/A",
            item['cat2'] if 'cat2' in item else "N/A")
        return item
