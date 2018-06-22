# -*- coding: utf-8 -*-
import re
import scrapy
import time
import tldextract
from copy import deepcopy
from scrapy.linkextractors import LinkExtractor

class FindspiderSpider(scrapy.Spider):
    name = 'findspider'
    # allowed_domains = ['baidu.com']
    search_content = input('查询关键字:')
    page = 35

    def start_requests(self):
        start_url = 'https://www.baidu.com/s?wd={}'.format(self.search_content)
        # headers = {}
        yield scrapy.Request(
            url=start_url,
            callback=self.parse
        )

    def parse(self, response):
        # 取得10个待解析url, 构建下一页url
        item = {}
        if self.page < 60:  # 总页数
            self.page += 1
            print(self.page, '<<当前页')
            div_list = response.xpath('//div[@id="content_left"]/div[contains(@class,"result")]')
            for div in div_list:
                old_url = div.xpath('./h3/a/@href').extract_first()
                print('old_url',old_url)
                yield scrapy.Request(
                    url=old_url,
                    # url='https://www.jx015.com/',
                    callback=self.parse_new_url,
                    meta={'item': deepcopy(item)},
                    dont_filter=True
                )
                break
            # next_url = 'https://www.baidu.com/s?wd={}&pn={}'.format(self.search_content,str(self.page*10))
            # print(next_url,'next_url')
            # if next_url is not None:
            #     yield scrapy.Request(
            #         url=next_url,
            #         callback=self.parse,
            #         meta={'item': deepcopy(item)}
            #     )

    def parse_new_url(self,response):
        # 解析跳转后的网址
        item = response.meta["item"]
        item['pre_url'] = response.url
        text = response.text

        num = 0
        if 'QQ' in text:
            # x = set(re.findall('QQ.{5,13}[0-9]', text.strip()))
            x = set(re.findall('QQ[\:\s0-9]{5,15}', text.strip()))
            print('QQ', x)
            if len(x)>0:
                for i in x:
                    key = 'QQ-' + str(num)
                    num += 1
                    item[key] = i
                num = 0
        if '微信' in text:
            # x = set(re.findall('微信[\:\u4e00-\u9fa5_a-zA-Z0-9]+', text.strip()))
            # 不含公众号，以中英文数字结尾
            x = set(re.findall('微信(?!公众号)[\:\s\u4e00-\u9fa5_a-zA-Z0-9]{2,17}[a-zA-Z0-9\u4e00-\u9fa5]', text.strip()))
            print('微信', x)
            if len(x) > 0:
                for i in x:
                    key = '微信-' + str(num)
                    num += 1
                    item[key] = i
                num = 0
        if 'qq' in text:
            print('qq', x)
            # x = set(re.findall('qq.{5,13}[0-9]', text.strip()))
            x = set(re.findall('qq[\:\s0-9]{5,15}', text.strip()))
            if len(x) > 0:
                for i in x:
                    key = 'qq-' + str(num)
                    num += 1
                    item[key] = i
                num = 0
        # print(item)
        yield item


    # def parse_get_content(self,response):
    #     item = response.meta["item"]
    #     if 'iframe' in response.text or 'IFRAME' in response.text:
    #     #  找到所有iframe
    #         l = re.findall('\<iframe(.*?)\<\/iframe\>', response.text, re.S)
    #         print('iframelist',l)
    #         for i in l:
    #             # print(i,l.index(i))
    #             url = re.findall('src\=\"(.*?)\"', i, re.S)[0] if len(re.findall('src\=\"(.*?)\"', i, re.S))>0 else None
    #             print(url)
    #             if url is not None:
    #                 if 'http' in url or 'https' in url:
    #                     yield scrapy.Request(
    #                         url=url,
    #                         callback=self.get_qq
    #                     )
    #
    #                 else:
    #                     print(item['real_url'])
    #                     print('get_content--url ',url)
    #                     url = item['real_url']+url
    #                     print('************')
    #                     print(url)
    #                     yield scrapy.Request(
    #                         url=url,
    #                         callback=self.get_qq
    #                     )
    #
    #
    # def get_qq(self,response):
    #     # pass
    #     # if 'qq:' in response.text:
    #     #     x=re.findall('qq.{5,20}[0-9]',response.text,re.S)
    #     #
    #     #     print(x)
    #     if 'QQ：' in response.text:
    #         x = re.findall('QQ.{5,20}[0-9]',response.text.strip())
    #         print(x,'QQ')
    #     if 'qq' in response.text:
    #         x = re.findall('qq.{5,20}[0-9]', response.text.strip())
    #         print(x, 'qq')
