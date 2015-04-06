from scrapy.spider import Spider
from scrapy.selector import Selector
from ..items import LinkItem
from scrapy.http import Request
from scrapy.cmdline import execute
import codecs
class BeerLinks(Spider):
	name = "beerLinks"
	allowed_domains = ["thebeerstore.ca"]
	start_urls = [
		"http://www.thebeerstore.ca/beers/search/all",
	]

	def parse(self, response):
            sel = Selector(response)
            item = LinkItem()
            for link in sel.xpath('//div[@class="brands-container"]//a/@href').extract():
                item['link'] = 'http://www.thebeerstore.ca' + str(link)
                yield item
