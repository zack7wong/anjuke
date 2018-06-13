# -*- coding: utf-8 -*-
import scrapy
import re
import time
from copy import deepcopy


class ZufangSpider(scrapy.Spider):
    name = 'zufang'
    # allowed_domains = []
    #
    start_urls = [
        # 'https://sh.zu.anjuke.com/fangyuan/l2/',
        # 'https://hz.zu.anjuke.com/fangyuan/l2/',
        # 'https://su.zu.anjuke.com/fangyuan/l2/',
        # 'https://nj.zu.anjuke.com/fangyuan/l2/',
        'https://wx.zu.anjuke.com/fangyuan/l2/',

        # 'https://sz.zu.anjuke.com/fangyuan/l2/',
        # 'https://gz.zu.anjuke.com/fangyuan/l2/',
        # 'https://fs.zu.anjuke.com/fangyuan/l2/',
        # 'https://cs.zu.anjuke.com/fangyuan/l2/',
        # 'https://san.zu.anjuke.com/fangyuan/l2/',  # 三亚
        # 'https://hui.zu.anjuke.com/fangyuan/l2/',  # 惠州
        # 'https://dg.zu.anjuke.com/fangyuan/l2/',  # 东莞
        # 'https://hk.zu.anjuke.com/fangyuan/l2/',  # 海口
        # 'https://zh.zu.anjuke.com/fangyuan/l2/',  # 珠海
        # 'https://zs.zu.anjuke.com/fangyuan/l2/',  # 中山
        # 'https://xm.zu.anjuke.com/fangyuan/l2/',  # 厦门
        # 'https://nn.zu.anjuke.com/fangyuan/l2/',  # 南宁
        # 'https://qz.zu.anjuke.com/fangyuan/l2/',  # 泉州
        # 'https://lzh.zu.anjuke.com/fangyuan/l2/', # 柳州
    ]
    # start_urls = [
        # 'https://am.zu.anjuke.com/fangyuan/l2/',
        # 'https://ans.zu.anjuke.com/fangyuan/l2/', #
        # 'https://ale.zu.anjuke.com/fangyuan/l2/', #
        # 'https://as.zu.anjuke.com/fangyuan/l2/',
        # 'https://ank.zu.anjuke.com/fangyuan/l2/', #
        # 'https://ab.zu.anjuke.com/fangyuan/l2/', #
        # 'https://aks.zu.anjuke.com/fangyuan/l2/', #
        # 'https://al.zu.anjuke.com/fangyuan/l2/',
        # 'https://aq.zu.anjuke.com/fangyuan/l2/',
        # 'https://ay.zu.anjuke.com/fangyuan/l2/'
    # ]

    headers = {
        'authority': 'wh.zu.anjuke.com',
        'method': 'GET',
        'path': '/fangyuan/l2/',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'cache-control': 'max-age=0',
        'accept-language': 'zh-CN,zh;q=0.9',
        'upgrade-insecure-requests': '1',
        'referer': 'https://www.anjuke.com/sy-city.html',
    }

    def start_requests(self):
        item = {}
        for url in self.start_urls:
            item['start_url'] = url
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                meta={'item':deepcopy(item)}
            )
            # break

    def parse(self, response):
        # print(response.url,'<<>response.url<><>')
        item = response.meta['item']
        if '访问验证' in response.text:
            print(response.url, '<><>验证码<>')
            print()
        # print(response.text)
        # print('user-agent-->',response.request.headers["User-Agent"])
        # print(response.body)
        a_list = response.xpath('//div[contains(@class,"itemmod")]')
        item['city'] = response.xpath('//div[@class="cityselect"]/div[@class="city-view"]/text()').extract_first()
        if item['city'] is not None:
            item['city']=item['city'].strip()
        for a in a_list:
            href = a.xpath('./a/@href').extract_first()
            yield scrapy.Request(
                url=href,
                callback=self.parse_detail,
                meta={'item': deepcopy(item)}
            )
            # break

        next_url = response.xpath('//a[text()="下一页 >"]/@href').extract_first()
        print('next_url',next_url)
        if next_url is not None:
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                meta={'item': item}
            )

    def parse_detail(self,response):
        # print(response.url)
        item = response.meta['item']
        # item = {}
        # print(response.text)
        # time.sleep(0.1)
        if len(response.text) < 100:
            time.sleep(3)
        if len(response.text) < 100:
            time.sleep(3)
        item['brokerPhone'] = re.findall('brokerPhone:\'([0-9]+)',response.text)[0] if \
            len(re.findall('brokerPhone:\'([0-9]+)',response.text)) > 0 else None
        if item['brokerPhone'] is not None:
            item['personal_name'] = response.xpath('//*[@class="personal-name"]/text()').extract_first()
            # item['house_title'] = response.xpath('//*[@class="house-title"]/text()').extract_first()
            res = response.xpath('//ul[@class="house-info-zufang cf"]/li[@class="full-line cf"]/span')[0]
            # 租金
            item['price'] = res.xpath('string(.)').extract_first()
            # 户型
            item['house_type'] = response.xpath('//ul[@class="house-info-zufang cf"]/li[2]/span[2]/text()').extract_first()
            # 面积
            item['area'] = response.xpath('//ul[@class="house-info-zufang cf"]/li[3]/span[2]/text()').extract_first()
            # 朝向
            item['direction'] = response.xpath('//ul[@class="house-info-zufang cf"]/li[4]/span[2]/text()').extract_first()
            # 楼层
            item['floor'] = response.xpath('//ul[@class="house-info-zufang cf"]/li[5]/span[2]/text()').extract_first()
            # 装修
            item['beautify'] = response.xpath('//ul[@class="house-info-zufang cf"]/li[6]/span[2]/text()').extract_first()
            # 小区名和位置
            # a = response.xpath('//ul[@class="house-info-zufang cf"]/li[8]//text()').extract()
            # b = ''.join(a).strip()
            # item['house_position'] = re.sub('\s','', b)
            a = response.xpath('//div[@class="p_1180 p_crumbs"]//text()').extract()
            item['house_position'] = ''.join(a).strip()
            # 发布时间
            x = response.xpath('//div[@class="right-info"]/text()').extract_first()
            if x is not None:
                item['release'] = re.findall('发布时间\：(.*)',x,re.S)[0]
            # print('item >>',item)
            yield item