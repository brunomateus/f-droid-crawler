# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from fdroid.items import AppItem
from datetime import datetime
import logging

logger = logging.getLogger('apps_without_first_date')

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

        src_index = None
        tech_index = None
        n_links = len(link_text)
        j = 0
        while (src_index == None or tech_index == None) and j < n_links:
            if link_text[j].upper() == 'SOURCE CODE':
                src_index = j
            if link_text[j].upper() == 'TECHNICAL INFO':
                tech_index = j
            j += 1

        item = AppItem()
        item['name'] = app_name.strip()
        item['summary'] = app_description.strip()
        item['last_version_name'] = versions_numbers[0].strip()
        item['last_version_number'] = versions_numbers[1].strip()
        item['last_added_on']  = versions_date[0].strip()
        item['last_download_url'] = download_urls[0].strip()
        item['first_added'] = versions_date[-1].strip()

        other_informations_links =  other_informations.css('::attr(href)').extract()
        if src_index:
            source_code = other_informations_links[src_index]
            item['source_repo'] = source_code.strip()
        if tech_index:
           tech_info = other_informations_links[tech_index]

        item['versions'] = versions

        request = scrapy.Request(tech_info, callback=self.parse_info_page)
        request.meta['start_date'] = response.meta['start_date']
        request.meta['item'] = item
        yield request

    def parse_info_page(self, response):
        item = response.meta['item']
        if response.status == 404:
            self.logger.error("{} tech info not avaliable not found {}".format(item['name'],response.url))
            yield item

        start_date = response.meta['start_date']
        
        vnames = response.css('h2 > span::attr(id)').extract()
        vcodes = response.css('h2 + p + p::text').extract()

        fields = response.css('#mw-content-text > div > div:nth-child(2) > p::text').extract()

        for f in fields:
            field = f.split(':')
            if len(field) == 2:
                (name, value) = field
                if name.upper() == 'ID':
                    package = value.strip()
                elif name.upper() == 'ADDED':
                    try:
                        first_added = datetime.strptime(value.strip(), '%Y-%m-%d')
                    except ValueError:
                        self.logger.error("{} data format wrong not avaliable {}[{}]".format(value.strip(), item['name'], response.url))
                        first_added = datetime.strptime(item['first_added'], '%Y-%m-%d')

        if first_added is None:
            logger.warning("{}[{}] does not have first_added".format(item['name'], response.url))

        elif first_added >= start_date:
            item['number_of_versions'] = len(vnames)
            item['first_added'] = first_added.strftime('%Y-%m-%d')
        
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
