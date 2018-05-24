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

        versions_array  = response.css('ul.package-versions-list > .package-version  > .package-version-header')
        versions_numbers = versions_array.css('a::attr(name)').extract()
        text_date = response.css('ul.package-versions-list > .package-version  > .package-version-header::text').extract()
        
        download_urls = response.css('ul.package-versions-list > .package-version  > .package-version-download a:first-child::attr(href)').extract()

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

        other_informations = response.css('.package-links .package-link > a')
        link_text = other_informations.css('::text').extract()

        for j in range(len(link_text)):
            if link_text[j].upper() == 'SOURCE CODE':
                break
        source_code = other_informations.css('::attr(href)').extract()[j]
   
        item = AppItem()
        item['name'] = app_name.strip()
        item['summary'] = app_description.strip()
        item['last_version_name'] = versions_numbers[0].strip()
        item['last_version_number'] = versions_numbers[1].strip()
        item['last_added_on']  = versions_date[0].strip()
        item['last_download_url'] = download_urls[0].strip()
        item['source_repo'] = source_code.strip()
        item['versions'] = versions

        tech_info = other_informations[len(other_informations) - 1].css('::attr(href)').extract()[0]

        request = scrapy.Request(tech_info, callback=self.parse_info_page)
        request.meta['item'] = item
        yield request

    def parse_info_page(self, response):
        item = response.meta['item']
        
        vnames = response.css('h2 > span::attr(id)').extract()
        vcodes = response.css('h2 + p + p::text').extract()
        package = response.css('#mw-content-text > div > div:nth-child(2) p:nth-child(2)::text').extract()[0].split(':')[1].strip()

        item['number_of_versions'] = len(vnames)

#        print("Retriving tech info:  %s versions found" % (item['number_of_versions']))

        if item['number_of_versions'] > 3:

            versions = item['versions'] 

            for i in range(3, len(vcodes)):
                vcode = vcodes[i].split(':')[1].strip()
                versions.append({ 'name': vnames[i],
                    'code': vcode,
                    'download_url': 'https://f-droid.org/archive/' + package + '_' + vcode + '.apk',
                    })

        yield item
