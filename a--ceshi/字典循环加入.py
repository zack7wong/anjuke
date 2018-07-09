# -*- coding: utf-8 -*-
import time

# a='abc'
# text ="abccc"
#
# count =0
# for i in a:
#     num = text.count(i)
#     if num > count:
#         count=num
#         x=i
#
# print(x)
# print(a.index(i),'111')
# print(count)


# for i in a:
#     print(text.count(i))
# max(a,key=lambda x :text.count(x))

title_list=['a','b']
r='aaabbbbccccc'
item={}


word_num = 0
while 1:
    count = 0
    word_num += 1
    if len(title_list)>0:
        for word in title_list:
            num = r.count(word)
            if num > count:
                count = num
                x = word
        key ='title_word{}'.format(word_num)
        item[key]= x
        numa = title_list.index(x)
        title_list.pop(numa)
    else:
        break

print(item)
