# -*- coding: utf-8 -*-
import os

import re
from PIL import Image
import pytesseract
#上面都是导包，只需要下面这一行就能实现图片文字识别

# tessdata_dir_config = '--tessdata-dir "/home/python/.virtualenvs/spider_py3/bin/pytesseract"'
# def image_to_string(image, lang=None, boxes=False, config=tessdata_dir_config):
filename='capture3.png'
# f1, f2 = os.path.splitext(filename)
# print(f1,f2)
image= Image.open(filename)

# # 切掉四周的黑边
# width = im.size[0]
# height = im.size[1]
# left = 4
# top = 4
# right = width - 4
# bottom = height - 4
# box = (int(left), int(top), int(right), int(bottom))
# im = im.crop(box)
# im = im.resize((width * 4, height * 4), Image.BILINEAR)
# im.save(f1 + '_step1' + f2)

# 转为灰度图
# imgry = im.convert('L')
# imgry.save(f1 + '_step2' + f2)
#
# # 去噪
# threshold = 140
# table = []
# for i in range(256):
#     if i < threshold:
#         table.append(0)
#     else:
#         table.append(1)
# out = imgry.point(table, '1')
# out.save(f1 + '_step3' + f2)

gray = image.convert('L')
#图像对象转化（L：8位像素，表示黑和白）
#可以参考：Python图像处理库PIL的基本概念介绍 - icamera0的博客 - CSDN博客
bw = gray.point(lambda x:0 if x<132 else 255,'1')#如果RGB数值小于140的变成1，否则是255。也就是将验证码背景变成白色，具体字符变成黑色。
bw.save('ac.png')

text = pytesseract.image_to_string(bw,lang='chi_sim+eng')
#  text=pytesseract.image_to_string(Image.open('test.png'),lang='eng')   #设置为英文或阿拉伯字母的识别
print(text)
print('*'*90)
if 'QQ' in text:
    x = re.findall('QQ.{5,20}[0-9]', text.strip())
    print(x, 'QQ')
if 'qq' in text:
    x = re.findall('qq.{5,20}[0-9]', text.strip())
    print(x, 'qq')

if '微信' in text:
    x = re.findall('微信.{2,20}', text.strip())
    print(x, '微信')
