# -*- coding: utf-8 -*-
import scrapy
import re,sys,io
from copy import deepcopy

import time
from scrapy.linkextractors import LinkExtractor
# from openpyxl import load_workbook
import xlrd
import tldextract
from company.settings import title_keywords_company,title_keywords_school

class CompanyspiderSpider(scrapy.Spider):
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码
    name = 'companyspider'
    allowed_domains = ['']
    #  增加詞庫選擇
    while True:
        title_keywords = input('请选择词库： 1 公司 2 学校 \n')
        if title_keywords =='1':
            title_keywords = title_keywords_company
            print('已选择 1 公司\n')
            break
        elif title_keywords =='2':
            title_keywords = title_keywords_school
            print('已选择 2 学校\n')
            break
        else:
            print('错误，重新输入')
    time.sleep(1)
    # print(title_keywords)
    while True:
        try:
            excel = input('提取的关键词保存到当前文件夹下的文件名+output.xlsx \n请输入excel文件名(带文件扩展名),'
                          '如文件不在当前文件夹,需带上路径: \n ')
            data = xlrd.open_workbook(excel)
            # data = xlrd.open_workbook("苏州企业.xlsx")
        except IOError:
            print('文件不存在或路径不对，请从新输入')
        except Exception as e:
            print(e)
        else:
            break
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    # doc_title = table.row_values(0)
    # print(doc_title)

    start_urls = []
    for i in range(1, nrows):
        start_urls.append('http://' + table.row_values(i)[1])
    # start_urls = ['http://www.zhongang.net/']

    def start_requests(self):
        for url in self.start_urls:
            start_url = url
            url_index_doc = self.start_urls.index(start_url)
            # url ='.'.join(tldextract.extract(start_url)
            item1 = {'url':url, 'url_index_doc':url_index_doc}
            # headers = {}
            yield scrapy.Request(
                url=start_url,
                callback=self.parse,
                meta={'item1': item1}
            )

    def parse(self, response):
        item = deepcopy(response.meta["item1"])
        # 匹配后的关键词
        match_words = []
        try:
            try:
                r = response.text
            except Exception as e:
                print(e, '编码错误')
            title = response.xpath('//title/text()').extract_first()
            if title is None:
                x = re.findall('location.href=\"(.*?)\"', r, re.S)[0] if len(
                    re.findall('location.href=\"(.*?)\"', r, re.S)) > 0 else None
                # print(x,'<')
                if x is None:
                    x = re.findall('location="/(.*?)\"', r, re.S)[0] if len(
                        re.findall('location="/(.*?)\"', r, re.S)) > 0 else None
                    # print(x,'<<')
                if x is not None:
                    url = response.url + '/' + x
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse,
                        dont_filter=True,
                        meta={'item1': item}
                    )
            else:
                title_list = re.findall("[\u4E00-\u9FA5\(\)]+", title, re.S)  # title里面的关键词列表
                # title_list = re.findall("([\u4E00-\u9FA5a-zA-Z0-9]+)", title, re.S)  # title里面的关键词列表
                print('title_list', title_list)
            if len(title_list) > 0:
                for i in title_list:
                    if len(i) < 2:
                        title_list.pop(i)
                # 取次数第一的词
                count = 0
                x = None
                for word in title_list:
                    num = r.count(word)
                    if num > count:
                        count = num
                        x = word
                # print(count, 'title最大词数目')
                item['title'] = x
                # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                keywords = response.xpath('//meta[@name="keywords"]/@content').extract_first()
                if keywords is None:
                    response.xpath('//meta[@name="Keywords"]/@content').extract_first()
                    # 两个地方取keywords，都取不到 放弃
                if keywords is not None:
                    keywords_list = re.findall("([\u4E00-\u9FA5\(\)]+)", keywords, re.S)  # 词列表,正则取汉字
                    keywords_list = list(set(keywords_list))  # 去重
                    print('keywords_list>>>',keywords_list)
                    if len(keywords_list) > 0:
                        for i in keywords_list:
                            if len(i) < 2:
                                keywords_list.pop(i)
                        # keywords>0,在body中找到频率最高的3个词
                        word_num = 0
                        while 1:
                            if keywords_list == []:
                                break
                            count = 0
                            word_num += 1
                            if word_num > 3:
                                break
                            for word in keywords_list:
                                # 找keywords中的词在body中出现的次数排前三
                                num = r.count(word)
                                if num > count:
                                    count = num
                                    x = word
                                key = 'keywords{}'.format(word_num)
                                # item['keywords1']
                                item[key] = x
                            if count > 0:
                                try:
                                    numa = keywords_list.index(x)
                                    keywords_list.pop(numa)
                                except Exception as e:
                                    print(e)
                        # if item.get('keywords2') is None:
                        #     if item['title'] is not None:
                        #         if item['title'] != item.get('keywords1'): # keywords2没有时，取title
                        #             item['keywords2'] = item['title']

                else:
                    item['keywords1'] = item['title']


                print("((("*20)
                # description = response.xpath('//head/meta[@name="description"]/@content').extract_first()
                # item['description'] = description
                # print('\u00bb | <')
                # copyrt = response.xpath("//*[contains(text(),'版权所有')]//text()").extract_first()
                # item['copyrt'] = copyrt
                # # print('版权所有', copyrt)

                # 提取当前页面所有2-6字的标题
                le = LinkExtractor()
                links = le.extract_links(response)
                for link in links:
                    # a = link.text.strip()
                    # 去掉汉字以外的特殊字符
                    a = ''.join(re.findall("([\u4E00-\u9FA5]+)", link.text, re.S))
                    # print('aaaa',a)
                    if 2 < len(a) < 5:
                        # print('aa', a)
                        for title_keyword in self.title_keywords:
                            # 如果2-6之间的词组 含有title_keywords中的关键词,则加入match_words中
                            if title_keyword in a:
                                match_words.append(a)

                # print('>提取到含列表关键词的3-5字标题>', match_words)
                # 含有关键词的词再去重
                unique_words = []
                if len(match_words) > 0:
                    for i in match_words:
                        if i not in unique_words:
                            unique_words.append(i)
                    item['unique_words'] = unique_words
                else:
                    item['unique_words'] = None
                # print(item)
                yield item
        except Exception as e:
            print(e, '--错误')
