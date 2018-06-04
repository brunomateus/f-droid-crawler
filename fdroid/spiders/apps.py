# -*- coding: utf-8 -*-
import scrapy
from .base import BaseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from fdroid.items import AppItem

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

    def parse_item(self, response):
        self.logger.info('Processing... ' + response.url)
        item_links = response.css('#full-package-list .package-header::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(response.urljoin(a+"/"), callback=self.parse_detail_page)

 
