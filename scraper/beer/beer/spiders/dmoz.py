from scrapy.spider import Spider
from scrapy.selector import Selector
from beer.items import BeerItem
from scrapy.http import Request
from scrapy.cmdline import execute
import codecs
class DmozSpider(Spider):
	name = "chug"
	allowed_domains = ["thebeerstore.ca"]
	start_urls = [
		"http://www.thebeerstore.ca/beers/search/all",
	]

	def gen_drink_callback(self, response):
            sel = Selector(response)
	    for container in sel.xpath('//tr[@class="odd" or  @class="even"]'):
                item = BeerItem()
                item['link'] = "www.thebeerstore.ca" + container.xpath('//link[@rel="canonical"]/@href').extract()[0].encode('ascii','replace')
                rvol = container.xpath('.//td[@class="size"]/text()').extract()[0].encode('ascii','replace')
                rvol = rvol.replace('?',' ').split()
                item['vol'] = int(rvol[0]) * int(rvol[-2])
                if (container.xpath('.//td[@class="price"]/text()').extract() == []):
                    item['price'] = float(container.xpath('.//span[@class="sale-price"]/text()').extract()[0].encode('ascii','replace')[10:])
                else:
                    item['price'] = float(container.xpath('.//td[@class="price"]/text()').extract()[0].encode('ascii','replace')[1:])
    
                item['name'] = container.xpath('//h1[@class="page-title"]/text()').extract()[0].encode('ascii','replace')
                
                cl = container.xpath('//span[@class="filter"]')
                item['Type'] = cl[-2].xpath('text()').extract()[0].encode('ascii','replace').replace('%','')
                try:
                    item['Style'] = cl[-3].xpath('text()').extract()[0].encode('ascii','replace').replace('%','')
                except IndexError:
                    None
                item['Country'] = cl[-1].xpath('text()').extract()[0].encode('ascii','replace').replace('%','')
                for det in container.xpath('//dd'):
                    label = det.xpath('preceding::dt[1]/text()').extract()[0].encode('ascii','replace')[:-1].split()[0]
                    val = det.xpath('text()').extract()[0].encode('ascii','replace').replace('%','')
                    item[label] = val
                yield item


	def parse(self, response):
            sel = Selector(response)
            for link in sel.xpath('//div[@class="brands-container"]//a/@href').extract():
                yield Request('http://thebeerstore.ca' + str(link), callback = self.gen_drink_callback)
