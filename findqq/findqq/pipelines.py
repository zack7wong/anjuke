# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from aip import AipOcr
from pymongo import MongoClient
client = MongoClient()
collection = client['liuhecai']['contact3']

png_md5_list = []


class FindqqPipeline(object):
    # def __init__(self):
    #     self.driver = webdriver.PhantomJS()

    def img_to_str(self,image_path):
        config = {
            'appId': '11405933',
            'apiKey': 'GaLmfAGu7rz85yLXiZ0gMEEz',
            'secretKey': '7emgbm0xDHedoIzRBklTIAu1wWWMKRyH'
        }
        client = AipOcr(**config)
        with open(image_path, 'rb') as fp:
            image = fp.read()
        result = client.basicGeneral(image)
        if 'words_result' in result:
            return '\n'.join([w['words'] for w in result['words_result']])

    def process_item(self, item, spider):
        # 先在response中找，找到任意一个就不调用识图，一个都没找到则调用百度识图

        # if len(item) > 1:
        #     collection.insert(item)
        #     print('save response2mongo ok')
        #     return item
        # else:
        driver = webdriver.PhantomJS()
        png_md5 = hashlib.md5(item.get('pre_url').encode()).hexdigest()
        save_fn = png_md5 + '.png'
        if png_md5 not in png_md5_list:
            png_md5_list.append(save_fn)
            # print('save_fn ', save_fn)
            url = 'http://a57a58b59r.cn/'
            # url = item.get('pre_url')
            if 'baidu.com' not in url and '.chinaz.com' not in url:
                driver.set_window_size(1200, 900)
                driver.get(url)
                print('url)) pre_url)》  ',url)
                driver.save_screenshot(save_fn)
                print('save_screenshot ok')
                driver.close()
                text = self.img_to_str(save_fn)
                # time.sleep(1)
                os.remove(save_fn)
                print('remove ok')
                # print(text)
                num=0
                if 'QQ' in text:
                    x =set(re.findall('QQ.{5,20}[0-9]', text.strip()))
                    print('QQ--', x)
                    if len(x) > 0:
                        for i in x:
                            key = 'QQ-' + str(num)
                            num += 1
                            item[key] = i
                        num = 0
                if '微信' in text:
                    x = set(re.findall('微信.{2,20}', text.strip()))
                    print('微信--',x)
                    if len(x) > 0:
                        for i in x:
                            key = '微信-' + str(num)
                            num += 1
                            item[key] = i
                        num = 0

                if 'qq' in text:
                    print('qq--',x)
                    x = set(re.findall('qq.{5,20}[0-9]', text.strip()))
                    if len(x) > 0:
                        for i in x:
                            key = 'qq-' + str(num)
                            num += 1
                            item[key] = i
                        num = 0

                # if len(item) > 1:
                collection.insert(item)
                print('shitu2mongo ok')
                return item

