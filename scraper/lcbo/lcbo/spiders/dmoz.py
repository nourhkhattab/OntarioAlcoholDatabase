from scrapy.spider import Spider
from scrapy.selector import Selector
from lcbo.items import LcboItem
from scrapy.http import Request
from scrapy.cmdline import execute

class DmozSpider(Spider):
	name = "alcoholic-spider"
	allowed_domains = ["foodanddrink.ca"]
	start_urls = [
		"http://www.foodanddrink.ca/lcbo-ear/lcbo/product/searchResults.do?style=LCBO.css&page=1&action=result&sort=sortedProduct&order=1&resultsPerPage=11000",
	]

	def gen_drink_callback(self, response):
            item = LcboItem()
            sel = Selector(response)
            item['retall'] = sel.xpath('//td[@class="main_font"][1]').extract()

	    yield item
			

	def parse(self, response):
            sel = Selector(response)
            for link in sel.xpath('//a[contains(@href, "&")]/@href').extract():
                yield Request('http://www.foodanddrink.ca' + str(link), callback = self.gen_drink_callback)
                
