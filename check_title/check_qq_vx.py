import xlrd
import xlwt
# 微信:A列 qq:C列,对比筛选过的,去重

# 已经检查过的vx,
data = xlrd.open_workbook("/home/python/Documents/vx-qq可用.xlsx")
table = data.sheets()[0]
nrows = table.nrows
ncols = table.ncols

vx_list = []
qq_list = []
for i in range(1, nrows):
    # print(table.cell(i,0).value)
    # break
    # vx
    if table.cell(i,0).ctype == 2:
        vx = int(table.cell(i,0).value)
    else:
        vx = table.cell(i,0).value
    vx_list.append(vx)
    # qq
    if table.cell(i, 2).ctype == 2:
        qq = int(table.cell(i, 2).value)
    else:
        qq = table.cell(i, 2).value
    qq_list.append(qq)
print(len(vx_list),vx_list)


file = xlwt.Workbook(encoding='utf8')
sheet = file.add_sheet('sheet name', cell_overwrite_ok=True)

while True:
    try:
        excel = input('检查qq.vx的文件名,\n')
        data = xlrd.open_workbook("/home/python/Documents/"+excel)
        # data = xlrd.open_workbook("/home/python/Documents/4959.xlsx")
    except IOError:
        print('文件不存在或路径不对，请从新输入')
    except Exception as e:
        print(e)
    else:
        break
table2 = data.sheets()[0]
nrows2 = table.nrows
ncols2 = table.ncols
n = 0
m = 0
for i in range(1,nrows2):
    # print(table.cell(i,0).value)
    # break
    # vx
    try:
        print(table2.cell(i, 0).ctype)
    # if table2.cell(i, 0).ctype is not None:
        if table2.cell(i,0).ctype == 2:
            vx = int(table2.cell(i,0).value)
        else:
            vx = table2.cell(i,0).value
        # print('vx',vx)
        if vx not in vx_list:
            n+=1
            sheet.write(n, 0, vx)


        if table2.cell(i, 2).ctype == 2:
            qq = int(table2.cell(i, 2).value)
        else:
            qq = table2.cell(i, 2).value
        # print('qq', qq)
        if qq not in qq_list:
            m+=1
            sheet.write(m, 2, qq)
    except Exception as e:
        print(e)

file.save('/home/python/Documents/vx_qq-output1.xlsx')
print('save ok')
