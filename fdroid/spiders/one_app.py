# -*- coding: utf-8 -*-
import scrapy
from fdroid.items import AppItem


class OneAppSpider(scrapy.Spider):
    name = 'one_app'
    allowed_domains = ['www.f-droid.org']
    start_urls = ['https://f-droid.org/en/packages/de.geeksfactory.opacclient/']

    def parse(self, response):
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
