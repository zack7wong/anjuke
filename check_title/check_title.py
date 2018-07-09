import xlrd
import requests
import xlwt
import time
from retrying import retry
# 检查excel中的title是否和网站一致,
# excel 0,url 2,title 8,js

class Check_Url_Re():
    def __init__(self,url,word_title,word_js,position):
        self.url = url
        self.word_title = word_title
        self.word_js = word_js
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }

    # @retry(stop_max_attempt_number=3)
    def _parse_url(self, url):
        r = requests.get(url, headers=self.headers, timeout=6)
        try:
            x = r.content.decode()
        except:
            print('gbk')
            x = r.content.decode('gbk')
        if len(x) < 100:
            r = requests.get(url, headers=self.headers, timeout=6)
            try:
                x = r.content.decode()
            except:
                print('gbk2')
                x = r.content.decode('gbk')
        # print(x)
        return x


    def parse_url(self, url):
        print(url)
        try:
            html = self._parse_url(url)
        except:
            html = None
        return html

    def run(self):
        c_time = str(time.strftime("%m-%d", time.localtime()))
        name = excel.split('.')[0]+'output.xlsx'

        response_con =self.parse_url(self.url)
#       检查 保存
        try:
            if self.word_js in response_con and self.word_title in response_con:
                print('都有')
                table1.write(position, 17, '都有')
                file.save(c_time+'_output.xlsx')
                time.sleep(0.3)
                print('save ok.')
        except Exception as e:
            print(e)

if __name__ == '__main__':
    while True:
        try:
            excel = input('检查的文件名,\n'
                          '如文件不在当前文件夹,需带上路径: \n ')
            data = xlrd.open_workbook(excel)
            # data = xlrd.open_workbook("/home/python/Desktop/镜像模板0619.xlsx")
            # data = xlrd.open_workbook("123_3.xlsx")
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
    word_title = []
    word_js = []

    # ----全部copy
    file = xlwt.Workbook(encoding='utf8')
    table1 = file.add_sheet('sheet name', cell_overwrite_ok=True)

    for i in range(0, nrows):
        for j in range(0, ncols):
            # print(CompanyspiderSpider.table.cell(i, j).value)
            table1.write(i, j, table.cell(i, j).value)  # 全部复制

    # -------------------------
    try:
        for i in range(0, nrows):
        # for i in range(4, 7):
            position = i
            url = 'http://' + table.row_values(i)[0]
            word_title = table.row_values(i)[2]
            word_js = table.row_values(i)[8]
            # abc =table.row_values(i)[17]

            # if abc !='都有':
            #     print(position,'<<<<')
            check_url_re = Check_Url_Re(url,word_title,word_js,position)
            check_url_re.run()
            # break
    except Exception as e:
        print(e)



