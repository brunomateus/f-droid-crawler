# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from fdroid.items import AppItem
from datetime import datetime

class BaseSpider(CrawlSpider):
    name = 'base'
    allowed_domains = ['f-droid.org']
    start_urls = ['http://f-droid.org/']
    handle_httpstatus_list = [404]

    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.visited_apps = 0
        self.success = 0
 
    def parse_detail_page(self, response):
        self.visited_apps +=1
        if response.status == 404:
            self.logger.error("Apps not found %s", response.url)
            return

        self.success += 1
        print("[ %s/%s ] - %s" %  (self.success, self.visited_apps, response.url))

        app_name = response.css('h3.package-name::text').extract()[0].strip()
        app_description = response.css('.package-summary::text').extract()[0].strip()

        download_urls = response.css('ul.package-versions-list > .package-version  > .package-version-download a:first-child::attr(href)').extract()
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

        for i in range(len(versions_date)):
            versions.append({ 'name': versions_numbers[2*i],
                'code': versions_numbers[2*i + 1].strip(),
                'download_url': download_urls[i].strip(),
                'added_on': versions_date[i].strip()
                })

            
        item = AppItem()
        item['name'] = app_name.strip()
        item['summary'] = app_description.strip()
        item['last_version_name'] = versions_numbers[0].strip()
        item['last_version_number'] = versions_numbers[1].strip()
        item['last_added_on']  = versions_date[0].strip()
        item['last_download_url'] = download_urls[0].strip()
        item['source_repo'] = source_code.strip()
        item['versions'] = versions
        yield item

