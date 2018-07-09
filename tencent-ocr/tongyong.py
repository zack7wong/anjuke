#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from qcloud_image import Client
from qcloud_image import CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers

appid = '1256964958'
secret_id = 'AKIDZ1IPL6K8VgfXEkMDBxXv8GDyX5UhaZEh'
secret_key = 'SmwwkMn25wb5QaZSccQ3UjmeLqDPQHwQ'
bucket = ''

client = Client(appid, secret_id, secret_key, bucket)
client.use_http()
client.set_timeout(30)

print('OCR-通用印刷体')
#  general_detect-》api-》files['url'] = pictures[0]
result = client.general_detect(CIUrls(['https://cdn2.jianshu.io/assets/web/web-note-ad-1-c2e1746859dbf03abe49248893c9bea4.png']))

# result = client.general_detect(CIFiles(['eg.png']))
if 'data' in result:
    print('\n'.join([w['itemstring'] for w in result['data']['items']]))
