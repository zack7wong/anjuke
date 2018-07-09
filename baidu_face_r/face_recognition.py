# -*- coding: UTF-8 -*-
# 文档
# http://ai.baidu.com/docs#/Face-Python-SDK/top

import base64

from aip import AipFace
# import cv2
# import matplotlib.pyplot as plt

APP_ID = '11441315'
API_KEY = 'Okrk4txQGgXrzCrgLkr6bEMG'
SECRET_KEY = 'mweV0d0TUMpBtpAgWTWH2s2hmEtf17kq'

# 初始化AipFace对象
aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
filePath = "ldh.jpg"

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 定义参数变量
options = {
    'max_face_num': 2, # 图像数量
    'face_field': "age,beauty,gender,quality,expression",
}
# 调用人脸属性检测接口
image = base64.b64encode(open('lyc.jpg', 'rb').read())
image = str(image,'utf-8')
imageType = "BASE64"
result = aipFace.detect(image,imageType,options)
print(result)

# 解析位置信息
# location=result['result'][0]['location']
# left_top=(location['left'],location['top'])
# right_bottom=(left_top[0]+location['width'],left_top[1]+location['height'])
#
# img=cv2.imread(filePath)
# cv2.rectangle(img,left_top,right_bottom,(0,0,255),2)
#
# cv2.imshow('img',img)
# cv2.waitKey(0)
# plt.imshow(img,"gray")
# plt.show()