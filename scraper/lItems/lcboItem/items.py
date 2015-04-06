# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class LcboItem(Item):
	link = Field()
        price = Field()
        alc = Field()
        form = Field()
        amount = Field()
        vol = Field()
        name = Field()
        Type = Field()
        cat1 = Field()
        cat2 = Field()
        ID = Field()
