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
        self.logger.info('Processing... ' + response.url)
        item_links = response.css('#full-package-list .package-header::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(response.urljoin(a), callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        app_name = response.css('h3.package-name::text').extract()[0].strip()
        app_description = response.css('.package-summary::text').extract()[0].strip()
        download_url = response.css('ul.package-versions-list > .package-version:first-child  > .package-version-download a:first-child::attr(href)').extract()
        
        other_informations = response.css('.package-links .package-link > a')
        link_text = other_informations.css('::text').extract()

        for j in range(len(link_text)):
            if link_text[j].upper() == 'SOURCE CODE':
                break
        source_code = other_informations.css('::attr(href)').extract()[j]

        versions_array  = response.css('ul.package-versions-list > .package-version  > .package-version-header')
        versions_numbers = versions_array.css('a::attr(name)').extract()
        text_date = response.css('ul.package-versions-list > .package-version  > .package-version-header::text').extract()
        
        versions_date = []
        versions = []

        for text in text_date:
            date = text.strip()
            if date:
                versions_date.append(date.split('on')[1])

        last_version_name = versions_numbers[0]
        last_version_code = versions_numbers[1]
        added_on = versions_date[0]

        for i in range(len(versions_date)):
            versions.append({ 'name': versions_numbers[i],
                'code': versions_numbers[i + 1],
                'added_on': versions_date[i]
                })

        item = AppItem()
        item['name'] = app_name
        item['summary'] = app_description
        item['last_version_name'] = last_version_name
        item['last_version_number'] = last_version_code
        item['last_added_on']  = added_on 
        item['download_url'] = download_url
        item['source_repo'] = source_code
        item['versions'] = versions
        yield item
