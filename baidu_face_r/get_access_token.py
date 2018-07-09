# import urllib, urllib2, sys
# import ssl
import requests
#
# # client_id 为官网获取的AK， client_secret 为官网获取的SK
# host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Okrk4txQGgXrzCrgLkr6bEMG&client_secret=mweV0d0TUMpBtpAgWTWH2s2hmEtf17kq'
# request = urllib2.Request(host)
# request.add_header('Content-Type', 'application/json; charset=UTF-8')
# response = urllib2.urlopen(request)
# content = response.read()
# if (content):
#     print(content)

url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Okrk4txQGgXrzCrgLkr6bEMG&client_secret=mweV0d0TUMpBtpAgWTWH2s2hmEtf17kq'

headers = {
    'Content-Type': "application/json",
    'charset': 'UTF-8'
}
r = requests.get(url,headers=headers)
print(r.content.decode())

"""
{
"access_token":"24.32b47419183015f0ac5964f12b4b284f.2592000.1532505813.282335-11441315",
"session_key":"9mzdCPa\/I46l9GwNAcJFLjkEVEpazY92B5gu2io4srAJqi+TV0uIS7M2xV50GMmdL9rYSLi9CdB9ijHty9uBR7M9pPEfNg==",
"scope":"public brain_all_scope vis-faceverify_faceverify_h5-face-liveness vis-faceverify_FACE_V3 wise_adapt lebo_resource_base lightservice_public hetu_basic lightcms_map_poi kaidian_kaidian ApsMisTest_Test\u6743\u9650 vis-classify_flower lpq_\u5f00\u653e cop_helloScope ApsMis_fangdi_permission smartapp_snsapi_base iop_autocar",
"refresh_token":"25.ddcc8611a8ba36768467c36ee94f8693.315360000.1845273813.282335-11441315",
"session_secret":"9fa9ef1ffb3a81549e53e8c1a6671da5",
"expires_in":2592000
}
"""