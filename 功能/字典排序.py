# -*- coding: utf-8 -*-

item = {'a':'aaa', 'b':'bb', 'c':'ccccccc'}
list = [item['a'],item['b'],item['c'],]
list2 = sorted(list, key=lambda x: len(x), reverse=True)
print(list2)