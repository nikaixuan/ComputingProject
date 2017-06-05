# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# the purpose of the class is to define the item
class BotItem(scrapy.Item):
    fromlist = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    crawled = scrapy.Field()
    spider = scrapy.Field()


