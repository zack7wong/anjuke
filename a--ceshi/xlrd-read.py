# https://mp.weixin.qq.com/s/MZlrpzCP-8EL_Wg_0ezE_w
import xlrd
from datetime import date, datetime

file = 'test.xls'

wb = xlrd.open_workbook(filename=file)#打开文件
print('获取所有表格名字: ', wb.sheet_names())

# sheet1 = wb.sheet_by_index(0)  # 通过索引获取表格
sheet1 = wb.sheets()[0]

sheet2 = wb.sheet_by_name('年级')  # 通过名字获取表格
print(sheet1, sheet2)
print(sheet1.name, sheet1.nrows, sheet1.ncols)   # 表格名,行数,列数

print('*****')
print(sheet1.row_values(1), '获取行内容')
print(sheet1.col_values(0), '获取列内容')


# 获取表格里的内容，三种方式
print(sheet1.cell(1, 2).value)
print(sheet1.cell_value(1, 0))
print(sheet1.row(1)[0].value)


# 读取excel中单元格内容为日期的方式
# ctype :  0 empty，1 string，2 number， 3 date，4 boolean，5 error
# print(sheet1.cell(1,2).ctype)
if sheet1.cell(1,2).ctype == 3:
    date_value = xlrd.xldate_as_tuple(sheet1.cell_value(1, 2), wb.datemode)
    print(date_value)
    print(date(*date_value[:3]))
    print(date(*date_value[:3]).strftime('%Y/%m/%d'))

# 获取合并单元格的内容
print(sheet1.merged_cells)
print(sheet1.cell_value(1,3))
print(sheet1.cell_value(4,3))
print(sheet1.cell_value(6,1))