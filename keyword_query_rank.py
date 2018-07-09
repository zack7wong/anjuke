import requests
import time
from lxml import etree
from retrying import retry
import xlrd,xlwt

class BaiduSearch(object):
    def __init__(self,search_word,excel_url,i,col_num):
        self.col_num = col_num
        self.i = i
        self.excel_url = excel_url
        self.search_word = search_word
        self.start_url = "https://www.baidu.com/s?word="+self.search_word+"&pn={}"
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

    def get_url_list(self):
        url_list = [self.start_url.format(i*10) for i in range(0, 10)]
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
        # print(num)
        div_list = html.xpath('//div[@id="content_left"]/div[contains(@class,"result")]')
        # j=0
        for div in div_list:
            # j+=1
            # print(j,'j')
            item = {}
            # name_list = div.xpath("./h3/a//text()") if len(div.xpath("./h3/a//text()")) >0 else None
            # item["item_name"] = "".join(name_list)
            # item["item_name"] = div.xpath('./h3/a//text()')[0] if len(div.xpath('./h3/a/em/text()')) > 0 else None
            item["item_url"] = div.xpath("./div//a[@class='c-showurl'][1]/text()")[0] if len(div.xpath("./div//a[@class='c-showurl'][1]/text()")) > 0 else None
            if item["item_url"] is not None:
                # print(item['item_url'],"item['url']")
                a = self.excel_url in item['item_url']
                # if j ==5:
                #     self.excel_url = 'www.cdsysyxx.com'
                # print(a,'<<<a')
                if a is True:
                    # print(self.excel_url, 'excel_url')
                    time.sleep(1)
                    table1.write(i, 16+int(col_num), num)
                    print('匹配到了"列"',16+int(col_num))
                    print(num,'num页')
                    # time.sleep(2)
                    # file.save('deo01.xls')
                    time.sleep(2)
                    return True

    def run(self):
        # 1 -10页
        url_list = self.get_url_list()
        for url in url_list:
            # 包含url时,保存当前页
            pre_num=url.split('=')[2]
            global num
            if pre_num == 0:
                num = 1
            else:
                num = int(pre_num)//10+1
                # print(num,'<<<num')

            html = self.parse_url(url)
            page_break = self.get_content_list(html)
            if page_break:
                file.save('demo01.xls')
                print('save ok')
                break

if __name__ == '__main__':
    while True:
        try:
            # excel = input('提取的关键词保存到当前文件夹下的output.xlsx \n请输入excel文件名(带文件扩展名),如文件不在当前文件夹,需带上路径: \n ')
            # data = xlrd.open_workbook(excel)
            # data = xlrd.open_workbook("/home/python/Desktop/23.xls")
            data = xlrd.open_workbook("/home/python/Desktop/镜像模板 -  已挂跳转js.xls")
            # data = xlrd.open_workbook("镜像模板 -  已挂跳转js.xls")
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
            table1.write(i, j, table.cell(i, j).value)  # 复制

    for i in range(1, nrows):
        excel_url = 'www.'+table.row_values(i)[0]
        print(excel_url,'excel_url')
        list = [table.row_values(i)[5],table.row_values(i)[6],table.row_values(i)[7]]
        # 取excel中的url,关键词
        for search_word in list:
            print(search_word)
            col_num=list.index(search_word) # 第几个词
            baidusearch = BaiduSearch(search_word,excel_url,i,col_num)
            baidusearch.run()
