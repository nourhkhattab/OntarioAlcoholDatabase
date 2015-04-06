# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from db.oadb import OADB

class BeerPipeline(object):

    def __init__(self):
        self.db = OADB()

    def close_spider(self, spider):
        self.db.endItems()
        self.db.close()

    def process_item(self, item, spider):
        self.db.addBeerItem(
            item['ID'],
            item['link'],
            item['name'],
            item['price'],
            item['amount'],
            item['vol'],
            item['form'],
            item['Alcohol'],
            item['Type'],
            [i for i in [item[j] for j in ["Style","Category"] if j in item]+["N/A"] if i][0])

        return item

