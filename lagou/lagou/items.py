# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    city = scrapy.Field()
    company = scrapy.Field()
    size = scrapy.Field()
    zone = scrapy.Field()
    createtime = scrapy.Field()
    labels = scrapy.Field()
    positionName = scrapy.Field()
    salary = scrapy.Field()
    education = scrapy.Field()
    workyear = scrapy.Field()

