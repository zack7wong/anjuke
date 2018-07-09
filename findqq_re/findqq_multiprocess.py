import hashlib
import os, re, time
from multiprocessing import Pool

import requests
from lxml import etree
from retrying import retry
import baidu_ocr
import image_split
from selenium import webdriver


from queue import Queue
import threading
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from setting import *


class FindQ:
    def __init__(self):
        self.cutting = image_split.Cutting()
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
        self.url_md5_list = []

        self.url_queue = Queue()
        self.html_queue = Queue()
        self.old_url_list_queue = Queue()
        self.new_content_queue = Queue()
        self.last_content_queue = Queue()

    def get_url_list(self, url_list):
        for url in url_list:
            self.url_queue.put(url)

    @retry(stop_max_attempt_number=3)
    def _parse_url(self, url):
        r = requests.get(url, headers=self.headers, timeout=5)
        return etree.HTML(r.content)

    def parse_url(self):
        while True:
            url = self.url_queue.get()
            try:
                html = self._parse_url(url)
            except:
                html = None
            self.html_queue.put(html)
            self.url_queue.task_done()  # 配合get计数减少1  


    def get_old_url(self):
        # 百度链接，跳转前的链接
        while 1:
            html = self.html_queue.get()
            if html is not None:
                li_list = html.xpath('//div[@id="content_left"]/div[contains(@class,"result")]')
                # old_url_list = []
                for li in li_list:
                    old_url = li.xpath('./h3/a/@href')[0] if len(li.xpath('./h3/a/@href')) > 0 else None
                    # old_url_list.append(old_url)
                    # break
                    self.old_url_list_queue.put(old_url)
            self.html_queue.task_done()

    @retry(stop_max_attempt_number=3)
    def parse_old_url(self):
        """
        :param url:
        :return: 跳转后的链接,响应内容
        """
        while 1:
            url = self.old_url_list_queue.get()

            try:
                r = requests.get(url, headers=self.headers1, timeout=8)
                new_url = r.url
                content_text = r.text
            except:
                new_url = None
                content_text = []

            if new_url is not None:
                item = {}
                item_1 = {}
                # new_url = 'http://www.ftyz.org/' ##大师傅
                url_md5 = hashlib.md5(new_url.encode()).hexdigest()

                if 'baidu.com' not in new_url and 'aizhan.com' not in new_url:
                    if url_md5 in self.url_md5_list:
                        print('url_md5 have seen')
                    else:
                        print('new_url', new_url)
                        self.url_md5_list.append(url_md5)
                        new_content = []
                        item["_id"] = url_md5
                        item['new_url'] = new_url
                        item["crawl_time"] = str(time.strftime("%Y-%m-%d %X", time.localtime()))

                        item_1['_id'] = url_md5
                        item_1['url'] = new_url
                        item_1["crawl_time"] = str(time.strftime("%Y-%m-%d %X", time.localtime()))

                        new_content.extend([new_url, item, item_1, content_text, url_md5])
                        # new_content.append(item_1) # 识图出错时移除md5
                        try:
                            collection_md5.insert(item_1)
                        except Exception as e:
                            print(e)
                        self.new_content_queue.put(new_content)
            self.old_url_list_queue.task_done()

    def savescreen_recognition(self,config):
        """
        保存截屏,截屏失败时，collection_md5移除当前url
        :param config:
        :return:
        """
        while True:
            print('# selenium截图,识别')
            # print('config', config)
            baiduocr = baidu_ocr.BaiduOcr(config)
            new_content = self.new_content_queue.get()
            print(111)
            if new_content is not None:
                new_url = new_content[0]

                item = new_content[1]
                item_1 = new_content[2]
                content = new_content[3]
                url_md5 = new_content[4]
                if len(content) > 0:
                    qq_list, QQ_list, vx_list = self.find_in_content(content)
                else:
                    qq_list = []
                    QQ_list = []
                    vx_list = []
                try:
                    desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
                    for key, value in self.headers1.items():
                        desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
                    driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities)
                    driver.set_window_size(1920, 1080)
                    driver.set_page_load_timeout(60)
                    driver.set_script_timeout(60)
                    print('selenium get url',new_url)
                    try:
                        driver.get(new_url)
                        driver.execute_script("""
                                    (function () {
                                        var y = 0;
                                        var step = 100;
                                        window.scroll(0, 0);

                                        function f() {
                                            if (y < document.body.scrollHeight) {
                                                y += step;
                                                window.scroll(0, y);
                                                setTimeout(f, 100);
                                            } else {
                                                window.scroll(0, 0);
                                                document.title += "scroll-done";
                                            }
                                        }

                                        setTimeout(f, 1000);
                                    })();
                                """)
                        for i in range(30):
                            if "scroll-done" in driver.title:
                                break
                            time.sleep(6)
                        print('selenium save png')
                    except TimeoutException:
                        driver.execute_script('window.stop()') #在页面停止加载后继续操作
                        print('超时,window stop')
                    #     todo md5移除逻辑问题
                    else:
                        png_name = url_md5 + '.png'
                        driver.save_screenshot(png_name)
                        print("save png_name ok")
                except Exception as e:
                    print(e)
                    print('selenium错误')
                    try:
                        collection_md5.remove(item_1)
                        os.remove(png_name)
                    except Exception as e:
                        print(e)
                        print('collection_md5/os remove 错误')
                    print('remove md5&png_name ok')
                finally:
                    driver.quit()

                #  分割图片,识别图片
                try:
                    if png_name:
                        print('png_name', png_name)
                        try:
                            png_list = self.cutting.cut_image(png_name)
                        except Exception as e:
                            print(e,'图片切割异常')
                            png_list = []
                        # print('png_list', png_list)
                        print('******对每张图片识别 × 保存××**')
                        if png_list is not []:
                            for png in png_list:
                                #  百度识图
                                try:
                                    text = baiduocr.img_to_str(png)
                                    os.remove(png)
                                except Exception as e:
                                    print(e,'image2str error')
                                    os.remove(png)

                                # 识别出vx，qq
                                if text is not None and len(text) > 1:
                                    if 'QQ' in text:
                                        x = re.findall('QQ[\:\f\r\t\v0-9]{5,15}[0-9]', text.strip())
                                        # print('ocr-QQ', x)
                                        QQ_list.extend(x)
                                    if '微信' in text:
                                        # x = re.findall('微信.{2,20}', text.strip())
                                        x = re.findall('(?:微信|微信号)[\：\:\f\r\t\v]{1,4}[\u4e00-\u9fa5\-_a-zA-Z0-9]{6,20}[a-zA-Z_\-0-9]',
                                                       text.strip())
                                        # print(x, '<<<<<<<< ocr-微信<<<<<<<<')
                                        vx_list.extend(x)
                                    if 'qq' in text:
                                        x = re.findall('qq.{5,15}[0-9]', text.strip())
                                        # print('ocr-qq', x)
                                        qq_list.extend(x)

                        os.remove(png_name)
                    # item['QQ'] = list(set(QQ_list))
                    item['vx'] = list(set(vx_list))
                    item['qq'] = list(set(qq_list))+list(set(QQ_list))
                    if item['vx'] == [] and item['qq'] == []:
                        print('    qq,vx都没有')
                    else:
                        self.save2mongo(item)
                        print('save2mongo ok')
                    print('百度识图完毕\n')
                except Exception as e:
                    print(e)
                    print('cut-regonize')
                    try:
                        os.remove(png_name)
                    except Exception as e:
                        print(e, '<<<<<')
                # finally:
                #     try:
                #         os.remove(png_name)
                #     except Exception as e:
                #         print(e)
            self.new_content_queue.task_done()

    def is_not_used(self):
        pass

    def find_in_content(self, content):
        # self.is_not_used()  # 避免警告
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
        return a, b, c

    def save2mongo(self, item):
        try:
            collection.insert(item)
        except Exception as e:
            print(e)
            print('保存到mongodb出错')

    def run(self, search_word, page_num):
        #  从mongodb取已经爬过的url
        start_url = 'https://www.baidu.com/s?wd={}'.format(search_word)
        url_temp = start_url + '&pn={}'
        # 2.百度搜索页数
        url_list = [url_temp.format(i * 10) for i in range(page_num)]
        print('总',len(url_list))
        result = collection_md5.find()
        try:
            for item in result:
                self.url_md5_list.append(item['_id'])
        except Exception as e:
            print(e)
            print('url.md5添加错误')
        print('md5_list添加ok')

        thread_list = []
        t_url_list = threading.Thread(target=self.get_url_list, args=(url_list,))
        thread_list.append(t_url_list)

        for i in range(9):
            t_html = threading.Thread(target=self.parse_url)
            thread_list.append(t_html)

        for i in range(9):
            t_get_old = threading.Thread(target=self.get_old_url)
            thread_list.append(t_get_old)

        for i in range(9):
            t_parse_old = threading.Thread(target=self.parse_old_url)
            thread_list.append(t_parse_old)

        # ------------------------ 多账号 -------------------
        for i in range(1):
            config = {
                'appId': '11405933',
                'apiKey': 'GaLmfAGu7rz85yLXiZ0gMEEz',
                'secretKey': '7emgbm0xDHedoIzRBklTIAu1wWWMKRyH'
            }
            t_screen_recog = threading.Thread(target=self.savescreen_recognition,args=(config,))
            thread_list.append(t_screen_recog)

        config_yy = {
            'appId': '11457104',
            'apiKey': '8yasyWM7tg8Lzb594bSbt1Na',
            'secretKey': '9LPagsGDECoN13Af8XREQea8p4Ae25uv'
        }
        config_zl = {
            'appId': '11464895',
            'apiKey': 'QIbfK49YH7B2roWHiKKplXvD',
            'secretKey': 'H6o0xU0K5huTZMvN7tWc1VDtirREUxfX'
        }

        config_lh = {
            'appId': '11477940',
            'apiKey': 'vwWWdDINRS2Hulkcv5AajFMX',
            'secretKey': 'wpOtyRF5jRGv2587ch4WRKQrvaBrj2Ig'
        }

        # ---------------------------------------------------

        t_screen_recog = threading.Thread(target=self.savescreen_recognition, args=(config_yy,))
        thread_list.append(t_screen_recog)
        t_screen_recog = threading.Thread(target=self.savescreen_recognition, args=(config_zl,))
        thread_list.append(t_screen_recog)
        t_screen_recog = threading.Thread(target=self.savescreen_recognition, args=(config_lh,))
        thread_list.append(t_screen_recog)

        # ---------------------------------------------------
        for t in thread_list:
            t.setDaemon(True)  # 设置守护线程，说明该线程不重要，主线程结束，子线程结束
            t.start()
        # t.join()
        for q in [self.url_queue, self.html_queue, self.old_url_list_queue, self.new_content_queue]:
            q.join()  # 让主线程等待，队列计数为0之后才会结束，否则会一直等待 


if __name__ == '__main__':
    print(str(time.strftime("%m-%d %X", time.localtime())))
    try:
        # for i in range(0, nrows):
        findq = FindQ()
        # page_num = input('输入要查的页码eg,81\n')
        # page_num = int(page_num)
        page_num = 81
        p = Pool(4)
        # 1.查词数量
        for i in range(49,58):
            word = table.row_values(i)[0]
            # collection = client['new'][word]
            p.apply_async(findq.run, args=(word,page_num,))
            print('查词 ', i, word)
        p.close()
        p.join()
    except Exception as e:
        print(e)
        print('-=-=-=')
    print(str(time.strftime("%m-%d %X", time.localtime())))






