import json
from pprint import pprint


data = {
    'name' : '中文',
    'shares' : 100,
    'price' : 542.23
}

# Python数据结构转换为JSON
json_str = json.dumps(data).encode()

print(json_str)
print('***')

# JSON数据转字典
print(json.loads(json_str.decode('utf8')))