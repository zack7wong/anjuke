# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrapy.spiderloader

process = CrawlerProcess(get_project_settings())

process.crawl('companyspider')
process.start()
