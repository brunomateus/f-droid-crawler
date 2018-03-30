# -*- coding: utf-8 -*-
import scrapy
from fdroid.items import AppItem


class OneAppSpider(scrapy.Spider):
    name = 'one_app'
    allowed_domains = ['www.f-droid.org']

    def __init__(self, package_list_file=None, *args, **kwargs):
        super(OneAppSpider, self).__init__(*args, **kwargs)
        if package_list_file:
            with open(package_list_file, "rt") as f:
                self.packages = [url.strip() for url in f.readlines()]
        else:
            print("Packages list file not informed. Usa -a package_list_file=path")
            exit

    def start_requests(self):
        for idx, package in enumerate(self.packages):
            url = 'https://www.f-droid.org/en/packages/%s' % package
            print("[ %s ] - %s" % (idx + 1, url))
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        app_name = response.css('h3.package-name::text').extract()[0].strip()
        app_description = response.css('.package-summary::text').extract()[0].strip()
        last_version_name = response.css('ul.package-versions-list > .package-version:first-child  > .package-version-header a:first-child::attr(name)').extract()
        added_on = response.css('ul.package-versions-list > .package-version:first-child  > .package-version-header::text').extract()
        last_version_code = response.css('ul.package-versions-list > .package-version:first-child  > .package-version-header a:nth-child(2)::attr(name)').extract()
        download_url = response.css('ul.package-versions-list > .package-version:first-child  > .package-version-download a:first-child::attr(href)').extract()

        item = AppItem()
        item['name'] = app_name
        item['summary'] = app_description
        item['version_name'] = last_version_name
        item['version_number'] = last_version_code
        item['added_on']  = added_on[len(added_on) - 1].strip().split('on')[1]
        item['download_url'] = download_url
        yield item
