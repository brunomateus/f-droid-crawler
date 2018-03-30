# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from fdroid.items import AppItem

class AppsSpider(CrawlSpider):
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
        print('Processing..' + response.url)
        item_links = response.css('#full-package-list .package-header::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(response.urljoin(a), callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        app_name = response.css('h3.package-name::text').extract()[0].strip()
        app_description = response.css('.package-summary::text').extract()[0].strip()
        last_version_name = response.css('ul.package-versions-list > .package-version:first-child  > .package-version-header a:first-child::attr(name)').extract()
        added_on = response.css('ul.package-versions-list > .package-version:first-child  > .package-version-header::text').extract()
        last_version_code = response.css('ul.package-versions-list > .package-version:first-child  > .package-version-header a:nth-child(2)::attr(name)').extract()

        item = AppItem()
        item['name'] = app_name
        item['summary'] = app_description
        item['version_name'] = last_version_name
        item['version_number'] = last_version_code
        item['added_on']  = added_on[len(added_on) - 1].strip().split('on')[1]

        yield item
