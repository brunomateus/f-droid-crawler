# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    summary = scrapy.Field()
    version_name = scrapy.Field()
    version_number = scrapy.Field()
    added_on = scrapy.Field()
    download_url = scrapy.Field()
