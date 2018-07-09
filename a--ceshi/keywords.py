# -*- coding: utf-8 -*-
import requests
from lxml import etree

class Keywords():
    def __init__(self,url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }
        # self.wb = load_workbook("/home/python/Desktop/a123.xlsx")
        # self.sheet = self.wb.active
        # self.url_list =[cell.value for cell in list(self.sheet.columns)[1]]

    def _parse_url(self, url):

        r = requests.get(url, headers=self.headers, timeout=5)
        assert r.status_code == 200
        return etree.HTML(r.content)

    def parse_url(self, url):
        print(url)
        try:
            html = self._parse_url(url)
        except:
            html = None
        return html

    def get_content(self,html):
        title = html.xpath('//head/title/text()')
        if title ==[]:
            if html.xpath('//body/title/text()') is not None:
                title = html.xpath('//body/title/text()')[0]

        keywords = html.xpath('//head/meta[@name="keywords"]/@content')
        if keywords == []:
            if html.xpath('//meta[@name="keywords"]/@content')[0] is not None:
                keywords = html.xpath('//meta[@name="keywords"]/@content')[0]

        copyrit = html.xpath("//*[contains(text(),'版权所有')]/text()")

        print('title', title)
        print('keywords',keywords)
        print('banquan',copyrit)

        word1 ='教育'
        word2 ='概'
        a="//a[contains(text(),'{}')]"

        #  找到nav
        nav = html.xpath(a.format(word1))
        if nav == []:
            nav = html.xpath(a.format(word2))
        c = nav.xpath("../../*")
        print(len(c), "*" * 30)
        #
        # if c ==[] or len(c)<3:
        #     c = b.xpath("../following-sibling::*")
        #     print(len(c),'>'*50+'父')





    def run(self):
        html = self.parse_url(self.url)
        a= self.get_content(html)



if __name__ == '__main__':
    url ='http://www.zjyzpcxx.com/'
    keywords = Keywords(url)
    keywords.run()