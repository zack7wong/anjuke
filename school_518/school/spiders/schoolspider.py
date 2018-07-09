# 1.keywords 3个都有,   2.按长度排序
import re
import scrapy
from copy import deepcopy
import tldextract
from scrapy.linkextractors import LinkExtractor
import xlrd
import io,sys


class SchoolspiderSpider(scrapy.Spider):
    name = 'schoolspider'
    allowed_domains = ['']

    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码 ubuntu不需要
    while True:
        try:
            # excel = input('提取的关键词保存到当前文件夹下的output.xlsx \n请输入excel文件名(带文件扩展名),如文件不在当前文件夹,需带上路径: \n ')
            # data = xlrd.open_workbook(excel)
            data = xlrd.open_workbook("镜像模板-5-17.xlsx")
        except IOError:
            print('文件不存在或路径不对，请从新输入')
        else:
            break

    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    doc_title = table.row_values(0)

    # ajax
    # start_urls = ['http://www.gdsty.cn']
    # 需要重新拼接
    # start_urls = ['http://www.dandelionschool.org']
    # 重定向
    # start_urls = ['http://www.cqhgzy.com']
    # 被黑
    # start_urls = ['http://www.zhirong.net/']
    # start_urls = ['http://www.gdcvi.net']

    start_urls = []
    for i in range(1, nrows):
        start_urls.append('http://'+table.row_values(i)[1])

    # ---
    # start_urls = [table.row_values(i)[1] for i in range(1, nrows)]
    # print(start_urls)
    # sheet = wb.active
    # start_urls = ['http://'+cell.value for cell in list(sheet.columns)[1]][1:]

    # 要匹配的关键词
    title_keywords = ['新闻', '资讯','学校','学院', '校园', '教师', '招聘', '设置', '师资', '教育', '教学', '校务', '信息','公开', '名师', '学子',
                      '风采', '科研', '概况', '党建', '课程','建设','德育','招生','访客','专业','导航','机构','服务','园地','家长']

    def start_requests(self):
        for url in self.start_urls:
            start_url = url
            # item1={'url':'.'.join(tldextract.extract(url))}
            # headers = {}
            url_index_doc = self.start_urls.index(url)
            item1 = {'url': url, 'url_index_doc': url_index_doc}
            # print(item1)
            yield scrapy.Request(
                url=start_url,
                callback=self.parse,
                meta={'item1': item1}
            )

    def parse(self, response):
        print(response.url, '    <<<<<<  response.url')
        item = deepcopy(response.meta["item1"])
        # 匹配后的关键词
        match_words = []
        try:
            try:
                r = response.text
                # r = response.body.decode()
                # print(r)
            # except UnicodeDecodeError :
            #     r = response.body.decode('gbk')
            except Exception as e:
                print(e, '编码错误')
            # body里面所有内容
            # b = re.findall("<body>(.*?)</body>", r, re.S)
            # b=''.join(b)
            # r = ''.join(r)
            title = response.xpath('//title/text()').extract_first()
            if title is None:
                x = re.findall('location.href=\"(.*?)\"',r,re.S)[0] if len(re.findall('location.href=\"(.*?)\"',r,re.S)) > 0 else None
                # print(x,'<')
                if x is None:
                    x = re.findall('location="/(.*?)\"',r,re.S)[0] if len(re.findall('location="/(.*?)\"',r,re.S)) > 0 else None
                    # print(x,'<<')
                if x is not None:
                    url = response.url+'/'+x
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse,
                        dont_filter=True,
                        meta={'item1':item}
                    )
            else:
                title_list = re.findall("[\u4E00-\u9FA5]+", title, re.S)  # title里面的关键词列表
                # title_list = re.findall("([\u4E00-\u9FA5a-zA-Z0-9]+)", title, re.S)  # title里面的关键词列表
                # print('title_list', title_list)
            if len(title_list) > 0:
                for i in title_list:
                    if len(i) < 2:
                        title_list.pop(i)
                count = 0
                x = None
                for word in title_list:
                    num = r.count(word)
                    if num > count:
                        count = num
                        x = word
                # print(count, 'title最大词数目')
                item['title'] = x
                # print("item['title']", item['title'])
                # max(title_list, key=lambda x: r.count(x))
                # if count > 1:
                keywords = response.xpath('//meta[@name="keywords"]/@content').extract_first()
                if keywords is None:
                    keywords = response.xpath('//meta[@name="Keywords"]/@content').extract_first()
                print('keywords --xpath提取内容: ', keywords)

                if keywords is not None:
                    # print("keywords>>>",keywords)
                    keywords_list = re.findall("[\u4E00-\u9FA5]+", keywords, re.S)  # 词列表,正则取汉字
                    # print('<<<keywords_list<<', keywords_list)
                    keywords_list=list(set(keywords_list))  # 去重
                    if len(keywords_list) > 0:
                        for i in keywords_list:
                            if len(i) < 2:
                                keywords_list.pop(i)
                        # keywords>0,在body中找到频率最高的3个词
                        word_num = 0
                        while 1:
                            if keywords_list ==[]:
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
                            if count > 0: # 排除keywords都查不到的情况
                                try:
                                    numa = keywords_list.index(x)
                                    keywords_list.pop(numa)
                                except Exception as e:
                                    print(e)

                        if item.get('keywords2') is None:
                            if item['title'] is not None:
                                if item['title'] != item.get('keywords1'):
                                    item['keywords2'] = item['title']

                else:
                    item['keywords1'] = None

                description = response.xpath('//head/meta[@name="description"]/@content').extract_first()
                item['description'] = description

                copyrt = response.xpath("//*[contains(text(),'版权所有')]/text()").extract_first()
                item['copyrt'] = copyrt
                # print('版权所有', copyrt)

                # 提取当前页面所有2-6字的标题
                le = LinkExtractor()
                links = le.extract_links(response)
                for link in links:
                    # a = link.text.strip()
                    # 去掉汉字以外的特殊字符
                    a = ''.join(re.findall("([\u4E00-\u9FA5]+)", link.text.strip(), re.S))
                    # print('aaaa',a)
                    if 2 < len(a) < 5:
                        for title_keyword in self.title_keywords:
                            # 如果2-6之间的词组 含有title_keywords中的关键词,则加入match_words中
                            if title_keyword in a:
                                match_words.append(a)

                # print('>>',match_words)
                # 含有关键词的词再去重，不用set
                unique_words = []
                if len(match_words) > 0:
                    for i in match_words:
                        if i not in unique_words:
                            unique_words.append(i)
                    item['unique_words'] = unique_words
                else:
                    item['unique_words'] = None

                # if len(match_words) > 0:
                #     unique_words = set(match_words)
                #     item['unique_words'] = unique_words
                # print('spider item',item)
                yield item
        except Exception as e:
            print(e, '--错误')


            # except :
            #     r = response.body.decode('gbk')
            #     print('gbk')
            #     # print(r)
            #     # body里面所有内容
            #     # b = re.findall("<body>(.*?)</body>", r, re.S)
            #     # b=''.join(b)
            #     r = ''.join(r)
            #     # item = {}
            #     # item['url'] = response.url
            #     title = response.xpath('//head/title/text()').extract_first()
            #     title_list = re.findall("([\u4E00-\u9FA5]+)", title, re.S) # title里面的关键词列表
            #     # 取技术最大的词
            #     count=0
            #     x =0
            #     for word in title_list:
            #         num = r.count(word)
            #         if num > count:
            #             count = num
            #             x = word
            #     print(count,'title最大词数目')
            #     item['title']= x
            #     # max(title_list, key=lambda x: r.count(x))
            #
            #     if count > 1:
            #         keywords = response.xpath('//head/meta[@name="keywords"]/@content').extract_first()
            #         keywords_list = re.findall("([\u4E00-\u9FA5]+)", title, re.S) # 词列表
            #         print(keywords_list, '<<<keywords_list<<')
            #         word_num = 0
            #         while 1:
            #             count = 0
            #             word_num += 1
            #             if word_num>3:
            #                 break
            #             if len(keywords_list) > 0:
            #                 for word in keywords_list:
            #                     num = r.count(word)
            #                     if num > count:
            #                         count = num
            #                         x = word
            #                 key = 'keywords{}'.format(word_num)
            #                 item[key] = x
            #                 numa = keywords_list.index(x)
            #                 keywords_list.pop(numa)
            #             else:
            #                 break
            #
            #
            #
            #
            #         description = response.xpath('//head/meta[@name="description"]/@content').extract_first()
            #         item['description'] = description
            #
            #         copyrt = response.xpath("//*[contains(text(),'版权所有')]/text()").extract_first()
            #         item['copyrt'] = copyrt
            #         print('版权所有', copyrt)
            #
            #         # 提取当前页面所有2-6字的标题
            #         le = LinkExtractor()
            #         links = le.extract_links(response)
            #         for link in links:
            #             a = link.text.strip()
            #             if 2 < len(a) <6:
            #                 for title_keyword in self.title_keywords:
            #                     if title_keyword in a:
            #                         match_words.append(a)
            #
            #         # print('>>',match_words)
            #         # 词去重
            #         unique_words = set(match_words)
            #         item['unique_words'] = unique_words
            #
            #         # print(item)
            #         yield item

            # print(match_words)






        # 1.确定导航栏  len()>0
        # a= response.xpath("//ul[contains(@id,'nav')]")
        # print("ul,nav")
        # if a ==[]:
        #     a = response.xpath("//div[contains(@class,'nav')]")
        #     print('div,nav')
        #     if a == []:
        #         a = response.xpath("//div[@id='menu']")
        #         print("div,menu")
        #         if a==[]:
        #             a = response.xpath("//ul[contains(@class,'nav')]")
        #             print('div,Nav')

        # 2.定位导航栏标题的a标签.
        # b = response.xpath(".//a[contains(text(),'首页')]")
        # if b == []:
        #     b= response.xpath(".//a[contains(text(),'概')]")
        # print('b>>',b)
        # print("-----",len(b))
        #
        # # 3.根据2步a标签的 取到兄弟标签
        # c = b.xpath("./following-sibling::*")
        # print(len(c), "*" * 30)
        #
        # if c ==[] or len(c)<3:
        #     c = b.xpath("../following-sibling::*")
        #     print(len(c),'>'*50+'父')
        #
        #     if c ==[] or len(c)<5:
        #         c = b.xpath("../../following-sibling::*")
        #         print(len(c),"父父")
        #
        #         if c == [] or len(c) < 5:
        #             c = b.xpath("../../../following-sibling::*")
        #             print(len(c),'父父父')



#"""
        # le = LinkExtractor(restrict_xpaths='//div[@id="menu"]') # 提取xpath选中区域下的链接
        # le = LinkExtractor()
        # le = LinkExtractor(allow_domains=['txedu.cn']) #过滤域名
        # links = le.extract_links(response)
        # print([link.url for link in links])
        # print(len(links),'链接总数')

        # for link in links:
        #     print(link.url)

            # if len(re.findall(".*?概况",link.text))>0:
            #     print('>>>',link.url, )
            #

        # item['link_num'] = len(links)
        # print(deepcopy(item))
        # print(item,'+++')
#"""