# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor

class LinkextspiderSpider(scrapy.Spider):
    name = 'linkextspider'
    allowed_domains = []
    # start_urls = ['http://www.cdgxbhxx.com/']
    start_urls = ['http://www.hnsdfz.org/index.html','http://www.exqxx.cn']
    # start_urls = ['http://www.exqxx.cn']
    title_keywords = ['新闻','学校','校园','教师','招聘','设置','师资','教育','教学','校务','公开','名师','学子','风采','科研','概况','党建','课程']


    def parse(self, response):
        match_words = []
        le = LinkExtractor()
        links = le.extract_links(response)
        for link in links:
            a = link.text.strip()
            if 2 < len(a) < 6:
                for title_keyword in self.title_keywords:
                    if title_keyword in a:
                        match_words.append(a)

        match_words=set(match_words)
        print(match_words)

    ######a--ceshi xpath
        # li_list= response.xpath('//div[@class="hc-sid"]/ul/li/a')[1:]
        # # print(li_list)
        # for li in li_list:
        #     a=li.xpath('./text()')
        #     print(a)
        #     # print(a.extract_first())
        #     break
        # **************************







        # a = response.xpath("//a[contains(text(),'首页')]/../../*")[1:]
        # for i in a:
        #     print(i.extract())
        #     break






        # for i in a:
        # le = LinkExtractor()
        # links = le.extract_links(response)
        # for link in links:
        #     print(link.text)
        # le = LinkExtractor(restrict_xpaths="") # 提取xpath选中区域下的链接
        # le = LinkExtractor(allow_domains=['txedu.cn']) #过滤域名
        # le = LinkExtractor(allow=(r'hr.tencent.com\/position.*?',))  # 正则提取链接
        #
        # links = le.extract_links(response)
        # # print([link.url for link in links])
        # # print(len(links),'链接总数')
        # for link in links:
        #     # print(link.url, '<<链接')
        #     a=link.text
        #     print(a)
        #     # b=a.encode('utf-8').decode('utf-8')
        #     # print('safis :%s' %b)
        #     # print(b,'wenb')
            # print(b, '<<<<文本>>>>')
            # if len(link.text.strip()) >5:
            #     print(link.text)



# -*- coding: utf-8 -*-
# import scrapy
# from scrapy.linkextractors import LinkExtractor
#
# class LinkextspiderSpider(scrapy.Spider):
#     name = 'linkextspider'
#     allowed_domains = []
#     start_urls = ['https://hr.tencent.com/position.php?&start=0#a']
#
#     def parse(self, response):
#         # le = LinkExtractor() # 默认提取所有
#         # le = LinkExtractor(restrict_xpaths='//div[@class="news"]') # 提取xpath选中区域下的链接
#         # le = LinkExtractor(allow_domains=['txedu.cn']) #过滤域名
#         le = LinkExtractor(allow=(r'hr.tencent.com\/position.*?',))  # 正则提取链接
#
#         links = le.extract_links(response)
#         # print([link.url for link in links])
#         # print(len(links),'链接总数')
#         for link in links:
#             # print(link.url, '<<链接')
#             # print(link.text,'<<<<文本>>>>')
#             if len(link.text.strip()) >5:
#                 print(link.text)

