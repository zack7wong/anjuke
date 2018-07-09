import requests
import time
from lxml import etree
from retrying import retry
import xlrd,xlwt
from queue import Queue
import threading

# lock = threading.Lock()


class BaiduSearch(object):
# class BaiduSearch(threading.Thread):
    def __init__(self,list):
        # threading.Thread.__init__(self)
        # list [1, '万博新体育手机用户', '万博体育最新版本', '万博体育app客户端下载', '007man.com']
        print("list",list)
        self.row = list[0]
        self.excel_url = list[4]
        self.words = list[1:4]
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "www.baidu.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
        }

    def get_url_list(self,url):
        url_list = [url.format(i*10) for i in range(0, 10)]
        return url_list

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

    def get_content_list(self,html):
        # print(col_num)
        div_list = html.xpath('//div[@id="content_left"]/div[contains(@class,"result")]')
        # j=0
        if div_list is not None:
            for div in div_list:
                item = {}
                # name_list = div.xpath("./h3/a//text()") if len(div.xpath("./h3/a//text()")) >0 else None
                # item["item_name"] = "".join(name_list)
                # item["item_name"] = div.xpath('./h3/a//text()')[0] if len(div.xpath('./h3/a/em/text()')) > 0 else None
                item["item_url"] = div.xpath("./div//a[@class='c-showurl'][1]/text()")[0] if len(div.xpath("./div//a[@class='c-showurl'][1]/text()")) > 0 else None
                # print(item["item_url"])
                if item["item_url"] is not None:
                    # print(item['item_url'],"item['url']")
                    a = self.excel_url in item['item_url']
                    if a is True:
                        # print('匹配到了"列"'col_num)
                        return True

    def run(self):
        # 1 -10页
        try:
            for word in self.words: # 3个线程处理3个词
                # lock.acquire()
                try:
                    print('word .',word)
                    col_num = self.words.index(word) # 第几个词,确定保存位置用
                    starturl = "https://www.baidu.com/s?word=" + word + "&pn={}"
                    url_list = self.get_url_list(starturl)
                    # print(url_list,'<<<< url_list')
                    for url in url_list:
                        pre_num=url.split('=')[2]
                        global num
                        if pre_num == 0:
                            num = 1
                        else:
                            num = int(pre_num)//10+1
                        # num -找到excel_url时,所在的页面数
                        # print(num,'<<<num')
                        html = self.parse_url(url)
                        if self.get_content_list(html):  # 找到就退出循环
                            print('匹配到了"列"', word, col_num)
                            time.sleep(0.5)
                            table1.write(self.row, 16 + col_num, num)
                            break
                    file.save('demo12.xls')

                    print('save ok')
                # finally:
                #     lock.release()
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    # 打开excel 读取数据
    while True:
        try:
            # excel = input('提取的关键词保存到当前文件夹下的output.xlsx \n请输入excel文件名(带文件扩展名),如文件不在当前文件夹,需带上路径: \n ')
            # data = xlrd.open_workbook(excel)
            # data = xlrd.open_workbook("/home/python/Desktop/23.xls")
            data = xlrd.open_workbook("/home/python/Desktop/镜像模板 -  已挂跳转js.xls")
            # data = xlrd.open_workbook("镜像模板-5-23全部跳转.xlsx")
        except IOError:
            print('文件不存在或路径不对，请从新输入')
        else:
            break
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    doc_title = table.row_values(0)

    file = xlwt.Workbook()
    table1 = file.add_sheet('sheet name', cell_overwrite_ok=True)
    for i in range(0, nrows):
        for j in range(0, ncols):
            table1.write(i, j, table.cell(i, j).value)  # 全部读取复制
    # --------------------

    row_list_queue = Queue()
    case_queue = Queue()
    def get_nrow_list():
        # 取每行的数据
        for i in range(1, nrows):# 按行遍历excel
            # list  0-row,1,2,3-word,4-excel_url
            row_list = [i,table.row_values(i)[5],table.row_values(i)[6],table.row_values(i)[7],table.row_values(i)[0]]
            # list [1, '万博新体育手机用户', '万博体育最新版本', '万博体育app客户端下载', '007man.com']
            row_list_queue.put(row_list)

    def case():
        # 实例化
        while 1:
            list = row_list_queue.get()
            baidusearch = BaiduSearch(list)
            case_queue.put(baidusearch)
            row_list_queue.task_done()

    def run():
        while 1:
            baidusearch = case_queue.get()
            baidusearch.run()
            case_queue.task_done()

    thread_list = []

    t_row_list = threading.Thread(target=get_nrow_list)
    thread_list.append(t_row_list)

    for i in range(20):
        t_case = threading.Thread(target=case)
        thread_list.append(t_case)

    for i in range(20):
        t_run = threading.Thread(target=run)
        thread_list.append(t_run)


    for t in thread_list:
        t.setDaemon(True) #设置守护线程，说明该线程不重要，主线程结束，子线程结束
        t.start()
    # t.join()
    for q in [row_list_queue,case_queue]:
        q.join()    #让主线程等待，队列计数为0之后才会结束，否则会一直等待 


