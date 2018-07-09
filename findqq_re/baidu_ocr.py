import re
from aip import AipOcr
# 接口说明
# https://cloud.baidu.com/doc/OCR/OCR-Python-SDK.html#.E6.8E.A5.E5.8F.A3.E8.AF.B4.E6.98.8E

class BaiduOcr:
    def __init__(self,config):
        # config = {
        #     'appId': '11405933',
        #     'apiKey': 'GaLmfAGu7rz85yLXiZ0gMEEz',
        #     'secretKey': '7emgbm0xDHedoIzRBklTIAu1wWWMKRyH'
        # }
        self.client = AipOcr(**config)

    def get_file_content(self,file):
        with open(file, 'rb') as fp:
            return fp.read()

    def img_to_str(self,image_path):
        image = self.get_file_content(image_path)
        result = self.client.basicGeneral(image)
        # result = self.client.webImageUrl('https://cdn2.jianshu.io/assets/web/web-note-ad-1-c2e1746859dbf03abe49248893c9bea4.png')

        if 'words_result' in result:
            return '\n'.join([w['words'] for w in result['words_result']])

if __name__ == '__main__':
    config = {
        'appId': '11405933',
        'apiKey': 'GaLmfAGu7rz85yLXiZ0gMEEz',
        'secretKey': '7emgbm0xDHedoIzRBklTIAu1wWWMKRyH'
    }
    baiduocr = BaiduOcr(config)
    text = baiduocr.img_to_str('eg.png')
    print(text)
    print('text^^^')