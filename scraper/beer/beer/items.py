# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class BeerItem(Item):
	link = Field()
        vol = Field()
        price = Field()
        name = Field()
        Category = Field()
        Type = Field()
        Style = Field()
        Country = Field()
        Brewer = Field()
        Alcohol = Field()
        Attributes = Field()
