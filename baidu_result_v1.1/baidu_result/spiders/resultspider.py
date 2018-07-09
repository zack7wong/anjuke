# -*- coding: utf-8 -*-
import re
import scrapy
import time
import tldextract
from copy import deepcopy
from scrapy.linkextractors import LinkExtractor

# 域名解析包
# LinkExtractor提取链接
# openpyxl 保存到excel

class ResultspiderSpider(scrapy.Spider):
    name = 'resultspider'
    allowed_domains = []
    # start_urls = ['http://baidu.com/']
    search_content = input('查询关键字:')
    page = 0

    def start_requests(self):
        start_url = 'https://www.baidu.com/s?ie=UTF-8&wd={}'.format(self.search_content)
        # headers = {}
        yield scrapy.Request(url=start_url,callback=self.parse)

    def parse(self, response):
        # 取得10个待解析url, 构建下一页url
        item = {}
        if self.page < 100:
            self.page += 1
            print(self.page, '<<当前页')
            div_list = response.xpath('//div[@id="content_left"]/div[contains(@class,"result")]')
            for div in div_list:
                old_url = div.xpath('./h3/a/@href').extract_first()
                # print(old_url)
                yield scrapy.Request(
                    url=old_url,
                    callback=self.parse_new_url,
                    meta={'item': deepcopy(item)},
                    dont_filter=True
                )
            next_url = 'https://www.baidu.com/s?ie=UTF-8&wd={}&pn={}'.format(self.search_content,str(self.page*10))
            # print(next_url,'next_url')
            if next_url is not None:
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse,
                    meta={'item': deepcopy(item)}
                )

    def parse_new_url(self,response):
        # 调包获取实际网址
        item = response.meta["item"]
        pre_url = response.url
        protocol = re.search('http.*?\/\/', pre_url).group(0) #取协议 http/https
        # print(pre_url)
        # print("-"*40)
        item['real_url'] = '.'.join(tldextract.extract(pre_url)) #
        item['real_url'] = protocol+item['real_url']  #拼接完整的url地址: https://www.111.com
        # print(item['real_url'],' < 实际网址 ')
        yield scrapy.Request(
            url=item['real_url'],
            callback=self.parse_url_num,
            meta={'item':deepcopy(item)},
        )

    def parse_url_num(self,response):

        item = response.meta["item"]
        yield item
        # print(item,'++只传部分+')
        # le = LinkExtractor(restrict_xpaths='//div[@class="news"]') # 提取xpath选中区域下的链接
        # le = LinkExtractor()
        # le = LinkExtractor(allow_domains=['txedu.cn']) #过滤域名
        # links = le.extract_links(response)
        # print([link.url for link in links])
        # print(len(links),'链接总数')
        # for link in links:
        #     print(link.url, '<链接')

    # def get_url_num(self,response):
    #     item = deepcopy(response.meta["item"])
    #     print(item,'+++')
    #     # le = LinkExtractor(restrict_xpaths='//div[@class="news"]') # 提取xpath选中区域下的链接
    #     # le = LinkExtractor()
    #     # le = LinkExtractor(allow_domains=['txedu.cn']) #过滤域名
    #     # links = le.extract_links(response)
    #     # print([link.url for link in links])
    #     # print(len(links),'链接总数')
    #     # for link in links:
    #     #     print(link.url, '<链接')
    #
    #     # item['link_num'] = len(links)
    #     # print(deepcopy(item))
    #     # print(item,'+++')
    #     # print(111)
    #     yield item