from openpyxl import Workbook

contents = {'百度权重_站长': '7', '360综合权重': '8', '360收录量': '2180000', '建站时间': '6371', '百度权重_爱站': '8', '搜狗收录量': '11506470'}

class Pyxl_excel(object):  # 设置工序一
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active    # 激活工作表
        self.ws.append(['百度权重_站长', '建站时间', '百度权重_爱站', '360综合权重', '360收录量', '搜狗收录量'])  # 设置表头

    def process_item(self, item):
        line = [item['百度权重_站长'],item['建站时间'],item['百度权重_爱站'],item['360综合权重'],item['360收录量'],item['搜狗收录量']]  # 把数据中每一项整理出来
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.wb.save('/home/python/Desktop/tuniu.xlsx')  # 保存xlsx文件
        # return item

if __name__ == '__main__':
    pyxl_excel = Pyxl_excel()
    pyxl_excel.process_item(contents)