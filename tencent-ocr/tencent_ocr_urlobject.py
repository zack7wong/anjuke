import time
import random
import hmac
import hashlib
import binascii
import base64

import requests


class Auth(object):
    def __init__(self, appid, sid, skey):
        self._appid, self._secretid, self._secretkey = str(appid), str(sid), str(skey)

    def get_sign(self, bucket, howlong=86400):
        """ GET REUSABLE SIGN

        :param bucket: 图片处理所使用的 bucket
        :param howlong: 签名的有效时长，单位 秒

        :return: 签名字符串
        """

        if howlong <= 0:
            raise Exception('Param howlong must be great than 0')

        now = int(time.time())
        rdm = random.randint(0, 999999999)

        text = 'a=' + self._appid + '&b=' + bucket + '&k=' + self._secretid + '&e=' + str(now + howlong) + '&t=' + str(
            now) + '&r=' + str(rdm) + '&f='
        hexstring = hmac.new(self._secretkey.encode('utf-8'), text.encode('utf-8'), hashlib.sha1).hexdigest()
        binstring = binascii.unhexlify(hexstring)
        return base64.b64encode(binstring + text.encode('utf-8')).rstrip(),text

class T_Ocr(object):
    def __init__(self):
        self.url = "http://recognition.image.myqcloud.com/ocr/general"
        self.payload = "{\"appid\":\"1256964958\",\"bucket\":\"test\",\"url\":\"https://cdn2.jianshu.io/assets/web/web-note-ad-1-c2e1746859dbf03abe49248893c9bea4.png\"}"
        self.headers = {
            # 'Host': 'recognition.image.myqcloud.com',
            'Authorization': "9JFYez3b0C9FQqyFfKWXSikkfnthPTEyNTY5NjQ5NTgmYj1saWxpJms9QUtJRFoxSVBMNks4VmdmWEVrTURCeFh2OEdEeVg1VWhhWkVoJmU9MTUyOTY1NTQ2OCZ0PTE1Mjk1NjkwNjgmcj00MjkzNzE5NiZmPQ==",
            'Content-Type': "application/json",
            'Cache-Control': "no-cache",
            'Postman-Token': "e03fb04c-709e-4395-aba5-1f0ea3b0011d"
        }
    def abc(self):
        response = requests.request("POST", self.url, data=self.payload, headers=self.headers)
        print(response.text)

if __name__ == '__main__':
    # a = Auth('1256964958','AKIDZ1IPL6K8VgfXEkMDBxXv8GDyX5UhaZEh','SmwwkMn25wb5QaZSccQ3UjmeLqDPQHwQ')
    # authorization,text = a.get_sign('lili')
    # print(authorization)
    t = T_Ocr()
    t.abc()


