# -*- coding: utf-8 -*-
import scrapy
import re
import time
# from copy import deepcopy


class ZufangSpider(scrapy.Spider):
    name = 'zufang'
    allowed_domains = []
    # start_urls = ['https://wh.zu.anjuke.com/fangyuan/l2/']
    start_urls = ['https://gz.zu.anjuke.com/fangyuan/l2/']
    headers = {
        # 'authority': 'wh.zu.anjuke.com',
        # 'method': 'GET',
        # 'path': '/fangyuan/l2/',
        # 'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'cache-control': 'max-age=0',
        'accept-language': 'zh-CN,zh;q=0.9',
        'upgrade-insecure-requests': '1',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers=self.headers,
            )

    def parse(self, response):
        # print(response.text)
        # print('user-agent-->',response.request.headers["User-Agent"])
        # print(response.body)
        a_list = response.xpath('//div[contains(@class,"itemmod")]')
        for a in a_list:
            href = a.xpath('./a/@href').extract_first()
            yield scrapy.Request(
                url=href,
                callback=self.parse_brokerPhone
            )
            # break

        next_url = response.xpath('//a[text()="下一页 >"]/@href').extract_first()
        print('next_url',next_url)
        if next_url is not None:
            # print(222)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
            )

    def parse_brokerPhone(self,response):
        item = {}
        # print(response.text)
        # time.sleep(0.1)
        if len(response.text) < 100:
            time.sleep(3)
        if len(response.text) < 100:
            time.sleep(3)
        item['brokerPhone'] = re.findall('brokerPhone:\'([0-9]+)',response.text)[0] if len(re.findall('brokerPhone:\'([0-9]+)',response.text)) > 0 else None
        if item['brokerPhone'] is not None:
            item['personal_name'] = response.xpath('//*[@class="personal-name"]/text()').extract_first()
            item['house_title'] = response.xpath('//*[@class="house-title"]/text()').extract_first()
            # 发布时间
            item['right_info'] = response.xpath('//div[@class="right-info"]/text()').extract_first()
            print(item)
            yield item