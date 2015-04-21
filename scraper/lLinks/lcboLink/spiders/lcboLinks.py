from scrapy.spider import Spider
from scrapy.selector import Selector
from ..items import LcboItem
from scrapy.http import Request
from scrapy.cmdline import execute

class LCBOLinkSpider(Spider):
	name = "alcoholic-spider"
	allowed_domains = ["foodanddrink.ca"]
	start_urls = [
		"http://www.foodanddrink.ca/lcbo-ear/lcbo/product/searchResults.do?style=LCBO.css&page=1&action=result&sort=sortedProduct&order=1&resultsPerPage=12000",
	]

	def parse(self, response):
            sel = Selector(response)
            item = LcboItem()
            for link in sel.xpath('//a[contains(@href, "&")]/@href').extract():
                item['link'] = 'http://www.foodanddrink.ca' + str(link)
                yield item                
