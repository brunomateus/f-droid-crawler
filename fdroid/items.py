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
    first_added = scrapy.Field()
    last_version_name = scrapy.Field()
    last_version_number = scrapy.Field()
    last_added_on = scrapy.Field()
    versions = scrapy.Field()
    last_download_url = scrapy.Field()
    source_repo = scrapy.Field()
    number_of_versions = scrapy.Field()
