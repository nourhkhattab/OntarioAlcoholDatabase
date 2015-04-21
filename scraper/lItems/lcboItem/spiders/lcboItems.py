from scrapy.spider import Spider
from scrapy.selector import Selector
from ..items import LcboItem
from scrapy.http import Request
from scrapy.cmdline import execute
from db.oadb import OADB

class LCBOItemSpider(Spider):
	name = "lcboItem"
	allowed_domains = ["foodanddrink.ca"]

	def __init__(self):
            self.db = OADB()
            self.start_urls = self.db.getLCBOLinks()

        def closed(self, reason):
            self.db.close()

	def parse(self, response):
            sel = Selector(response)
            item = LcboItem()
            link = response.url
	    if "gift" in link or "vintagesshoponline":
                return
            dID = self.db.getID(link)
            item['ID'] = dID
            sel = Selector(response)
            item["link"]=sel.xpath('//input[@name="itemNumber"]/@value').extract()[0]
            container = sel.xpath('//td[@class="main_font"][1]')
            if container.re(r'PRODUCT DISCONTINUED') != [] or container.re(r'N/A%') != []:
                # code for discontinued
                self.db.setVisited(dID)
                return
            try:
                item["price"] = float(container.re('(?<=\$ )[\d|\.]*')[0])
            except:
                self.db.setVisited(dID)
                return
            item["alc"] = float(container.re('\d+\.\d+(?=%)')[0])
            item["form"] = container.re('(?<=mL ).*(?=\r)')[0]
            amount = container.re('\dx\d')
            if amount == []:
                item["amount"] = 1
            else:
                item["amount"] = int(container.re('\d+(?=x\d+)')[0])
            item["vol"] = int(container.re('\d+(?= mL)')[0])
            item["name"] = container.xpath('//span[@class="titlefont"]/text()').extract()[0]
            line = container.re('[^>]+(?=<br>[^,]+\d+\.\d+%)')
	    try:
                line = line[-1].lstrip().split(",")
                i = 0
                for e in line:
                    if i == 0:
                        item["Type"] = e
                    elif i == 1:
                        item["cat1"] = e.lstrip()
                    elif i == 2:
                        item["cat2"] = e.lstrip()
                    i+= 1
            except:
                item["Type"] = line   

	    yield item
            self.db.setVisited(dID)
