# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy

class MhwzspiderSpider(scrapy.Spider):
    name = 'mhwzspider'
    allowed_domains = ['www.mhwz.cn']
    start_urls = ['http://www.mhwz.cn/category/']

    def parse(self, response):
        div_list = response.xpath('//div[@id="allcate"]/div[1]') # 大分类列表
        for div in div_list:
            item = {}
            # item['b_cate'] = div.xpath('./h2/a/text()').extract_first() #大分类名
            li_list = div.xpath('./ul/li[1]')  # 小分类列表
            for li in li_list:
                item['sm_cate'] = li.xpath('./a/text()').extract_first() #小分类名 -音乐欣赏
                item['list_url'] = 'http://www.mhwz.cn'+ li.xpath('./a/@href').extract_first() # 点击小分类拿到 列表页url
                yield scrapy.Request(
                    item['list_url'],
                    callback=self.parse_list,
                    meta={'item': deepcopy(item)}
                )


    def parse_list(self, response):         ## 列表页--》详情页处理和拿到下一页url
        item = deepcopy(response.meta['item'])
        li_list = response.xpath('//div[@class="list"]/li')
        for li in li_list:
            item['detail_url'] = 'http://www.mhwz.cn'+li.xpath('./div[@class="site"]/h5/a/@href').extract_first()
            item['name'] = li.xpath('./div[@class="site"]/h5/a/text()').extract_first()
            yield scrapy.Request(
                item['detail_url'],
                callback=self.parse_details,
                meta={'item': deepcopy(item)}
            )

        next_url = response.xpath('//a[@title="下一页"]/@href').extract_first()
        print('http://www.mhwz.cn'+next_url, '<< next_url')
        if next_url is not None:
            next_url = 'http://www.mhwz.cn'+next_url
            # print(next_url,'<<<')
            yield scrapy.Request(
                next_url,
                callback=self.parse_list,
                meta={'item': deepcopy(item)}
            )

    def parse_details(self, response):
        item = deepcopy(response.meta['item'])
        # print(item)
        item['site_name'] = response.xpath('//div[@class="siteinfo"]/li[text()="网站名称:"]//span/text()').extract_first()
        # # print(item['site_name'])
        item['site_url'] = response.xpath('//div[@class="siteinfo"]/li[text()="网站域名:"]//span/text()').extract_first()
        # item['intro'] = response.xpath('//div[@class="info"]//text()').extract_first()
        # print(item)
        yield item