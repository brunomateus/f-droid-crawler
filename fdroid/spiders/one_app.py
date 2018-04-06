# -*- coding: utf-8 -*-
import scrapy
from .base import BaseSpider
from fdroid.items import AppItem


class OneAppSpider(BaseSpider):
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
            yield scrapy.Request(url=url, callback=self.parse_detail_page)

    
