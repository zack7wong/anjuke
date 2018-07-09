import base64
import os
import time
import datetime
import requests


def convert_local_image(image):
    # 原始图片 ==> base64 编码
    with open(image, 'rb') as f:
        image_data = f.read()
        base64_data = base64.b64encode(image_data)
        fout = open('base64_content.txt', 'wb')
        fout.write(base64_data)
        fout.close()

    # base64 编码 ==> 原始图片
    # with open('base64_content.txt', 'rb') as fin:
    #     base64_data = fin.read()
    #     ori_image_data = base64.b64decode(base64_data)
    #     fout = open('base64.png', 'wb')
    #     fout.write(ori_image_data)
    #     fout.close()


def convert_web_image():
    png_url = 'https://cdn2.jianshu.io/assets/web/web-note-ad-1-c2e1746859dbf03abe49248893c9bea4.png'
    r = requests.get(png_url, stream=True)
    if r.status_code == 200:
        image_data = r.content
        base64_data = base64.b64encode(image_data)
        # ##下载图片到本地
        with open('web.png', 'wb') as f:
            f.write(image_data)
        # ##将图片的 base64 编码保存到本地文件
        with open('web.txt', 'w') as fout:
            fout.write(base64_data)


if __name__ == '__main__':
    # convert_local_image()
    # convert_local_image('eg.png')
    a = os.path.getsize('base64.png')/1000
    print(int(a))
    print(type(a))

# MIME主要使用两种编码转换方式----Quoted-printable和Base64----将8位的非英语字符转化为7位的ASCII字符。
# Base64将三个字节转化成四个字节，因此Base64编码后的文本，会比原文本大出三分之一左右
