# -*- coding: utf-8 -*-
import scrapy
from .base import BaseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from fdroid.items import AppItem
from datetime import date
from datetime import datetime

class AppsSpider(BaseSpider):
    name = 'apps'
    allowed_domains = ['f-droid.org']
    start_urls = ['https://f-droid.org/en/packages']

    rules = (
            Rule(LinkExtractor(allow=('en/packages/'), restrict_css=('li.nav.next > a',)),
            callback="parse_item",
            follow=True),
            Rule(LinkExtractor(allow=(), deny=('en/packages/[0-9]/'), restrict_css=('nav.site-nav > a:first-child',)),
            callback="parse_item",
            follow=False),
        )

    def __init__(self, start_date=None, *args, **kwargs):
        super(AppsSpider, self).__init__(*args, **kwargs)
        self.start_date = date.min
        if start_date:
            self.start_date = start_date

    def parse_item(self, response):
        self.logger.info('Processing... ' + response.url)
        item_links = response.css('#full-package-list .package-header::attr(href)').extract()
        for a in item_links:
            request = scrapy.Request(response.urljoin(a+"/"), callback=self.parse_detail_page)
            request.meta['start_date'] = self.start_date
            yield request

 
