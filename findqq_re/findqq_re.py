import hashlib
import os, re, time
import requests
from lxml import etree
from retrying import retry
import baidu_ocr
import image_split
from selenium import webdriver
from pymongo import MongoClient


class FindQ:
    def __init__(self, search_content):
        self.start_url = 'https://www.baidu.com/s?wd={}'.format(search_content)
        self.url_temp = self.start_url + '&pn={}'
        self.url_list = [self.url_temp.format(i * 10) for i in range(81)]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.baidu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        self.headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }

    @retry(stop_max_attempt_number=3)
    def _parse_url(self, url):
        r = requests.get(url, headers=self.headers, timeout=5)
        return etree.HTML(r.content)

    def parse_url(self, url):
        try:
            html = self._parse_url(url)
        except:
            html = None
        return html

    def find_in_content(self, content):
        a = []
        b = []
        c = []
        if 'qq' in content:
            a = re.findall('qq[\:\f\r\t\v0-9]{5,15}[0-9]', content.strip())
            print('qq_list', a)
        if 'QQ' in content:
            b = re.findall('QQ[\:\f\r\t\v0-9]{5,15}[0-9]', content.strip())
            print('QQ_list', b)
        if '微信' in content:# 6-20个字母数字下划线或者减号，字母开头
            c = re.findall('(?:微信|微信号)[\：\:\f\r\t\v]{1,4}[\u4e00-\u9fa5\-_a-zA-Z0-9]{6,20}[a-zA-Z_\-0-9]',content.strip())
        return a, b,c

    def get_old_url(self, html):
        # 百度链接，跳转前的链接
        li_list = html.xpath('//div[@id="content_left"]/div[contains(@class,"result")]')
        old_url_list = []
        for li in li_list:
            old_url = li.xpath('./h3/a/@href')[0] if len(li.xpath('./h3/a/@href')) > 0 else None
            old_url_list.append(old_url)
            # break
        return old_url_list

    @retry(stop_max_attempt_number=3)
    def parse_old_url(self, url):
        """
        :param url:
        :return: 跳转后的链接,响应内容
        """
        try:
            r = requests.get(url, headers=self.headers1, timeout=6)
            new_url = r.url
            content = r.text
        except:
            new_url = None
            content = []
        return new_url, content

    def save2mongo(self, item):
        try:
            collection.insert(item)
        except Exception as e:
            print(e)

    def run(self):
        cutting = image_split.Cutting()
        config = {
            'appId': '11405933',
            'apiKey': 'GaLmfAGu7rz85yLXiZ0gMEEz',
            'secretKey': '7emgbm0xDHedoIzRBklTIAu1wWWMKRyH'
        }
        baiduocr = baidu_ocr.BaiduOcr(config)
        #  从mongo取已经爬过的
        result = collection_md5.find()
        url_md5_list = []
        for item in result:
            url_md5_list.append(item['_id'])
        try:
            for url in self.url_list:
                print('列表页url>>>>>>>>', url)
                html = self.parse_url(url)
                old_url_list = self.get_old_url(html)
                # print(old_url_list)
                item = {}
                for url in old_url_list:
                    # 解析得到new_url
                    new_url, content = self.parse_old_url(url)
                    if new_url is not None:
                        # new_url = 'http://www.ftyz.org/' ##大师傅
                        item['new_url'] = new_url
                        print('new_url', new_url)
                        url_md5 = hashlib.md5(new_url.encode()).hexdigest()
                        if 'baidu.com' not in new_url and 'aizhan.com' not in new_url:
                            # TODO url md5改存到数据库，全部存
                            if url_md5 in url_md5_list:
                                print('url_md5 have seen')
                            else:
                                url_md5_list.append(url_md5)
                                item1 = {}
                                item1['url'] = new_url
                                item1['_id'] = url_md5
                                try:
                                    collection_md5.insert(item1)
                                except Exception as e:
                                    print(e)
                                item["_id"] = url_md5
                                item["crawl_time"] = str(time.strftime("%Y-%m-%d %X", time.localtime()))
                                # 在response中找qq,和识图合并
                                if len(content) > 0:
                                    qq_list, QQ_list, vx_list = self.find_in_content(content)
                                else:
                                    qq_list = []
                                    QQ_list = []
                                    vx_list = []
                                print('# selenium截图')
                                driver = webdriver.PhantomJS()
                                driver.set_window_size(1200, 900)
                                driver.set_page_load_timeout(200)
                                print('selenium get url')
                                try:
                                    driver.get(new_url)
                                    print('selenium save png')
                                    driver.save_screenshot('a.png')
                                    print("save png ok")
                                except Exception as e:
                                    print(e)
                                    try:
                                        collection_md5.remove(item1)
                                    except Exception as e:
                                        print(e)
                                    print('remove ok')
                                finally:
                                    driver.quit()
                                #  分割图片
                                try:
                                    png_list = cutting.cut_image('a.png')
                                    print('png_list', png_list)
                                    print('******对每张图片识别 × 保存××**')
                                    for png in png_list:
                                        #  百度识图
                                        text = baiduocr.img_to_str(png)
                                        os.remove(png)

                                        if text is not None and len(text) > 1:
                                            if 'QQ' in text:
                                                x = re.findall('QQ[\:\f\r\t\v0-9]{5,15}[0-9]', text.strip())
                                                print('ocr-QQ', x)
                                                QQ_list.extend(x)
                                            if '微信' in text:
                                                # x = re.findall('微信.{2,20}', text.strip())
                                                x = re.findall('(?:微信|微信号)[\：\:\f\r\t\v]{1,4}[\u4e00-\u9fa5\-_a-zA-Z0-9]{6,20}[a-zA-Z_\-0-9]', text.strip())
                                                print(x, '<<<<<<<< ocr-微信<<<<<<<<')
                                                vx_list.extend(x)

                                            if 'qq' in text:
                                                x = re.findall('qq.{5,15}[0-9]', text.strip())
                                                print('ocr-qq', x)
                                                qq_list.extend(x)
                                    print('百度识图完毕')
                                except Exception as e:
                                    print(e)
                                item['QQ'] = list(set(QQ_list))
                                item['vx'] = list(set(vx_list))
                                item['qq'] = list(set(qq_list))
                                self.save2mongo(item)
                                print('save2mongo ok')
        except Exception as e:
            print(e)

if __name__ == '__main__':
    print(str(time.strftime("%m-%d %X", time.localtime())))
    search_content = input('查询关键字:')
    client = MongoClient()
    collection = client['find'][search_content]
    collection_md5 = client['find']['url_md5']
    findq = FindQ(search_content)
    findq.run()
    print(str(time.strftime("%m-%d %X", time.localtime())))


#     vx_list
