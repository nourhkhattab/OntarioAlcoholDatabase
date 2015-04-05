# Scrapy settings for tdsb project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'beer'

SPIDER_MODULES = ['beer.spiders']
NEWSPIDER_MODULE = 'beer.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tdsb (+http://www.yourdomain.com)'
