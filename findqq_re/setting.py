import xlrd
from pymongo import MongoClient


client = MongoClient(host='localhost', port=27017, connect=False)
# 去重
collection_md5 = client['new']['url_md5']

collection = client['new']['8590']


while True:
    try:
        excel = input('查找的excel文件名:\n')
        # data = xlrd.open_workbook(excel)
        data = xlrd.open_workbook("/home/python/Desktop/627-findqq-vx.xlsx")
    except IOError:
        print('文件不存在或路径不对，请从新输入')
    except Exception as e:
        print(e)
    else:
        break
table = data.sheets()[0]
nrows = table.nrows
ncols = table.ncols
