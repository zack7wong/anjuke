# -*- coding: utf-8 -*-
r= 'aabbbb'
keywords_list=['a','b']

item={}
word_num = 0
while 1:
    count = 0
    word_num += 1
    if word_num > 3:
        break
    for word in keywords_list:
        # 找keywords中的词在body中出现的次数排前三
        num = r.count(word)
        if num > count:
            count = num
            x = word
        key = 'keywords{}'.format(word_num)
        # item['keywords1']
        item[key] = x
    try:
        numa = keywords_list.index(x)
        keywords_list.pop(numa)
    except Exception as e:
        print(e)

print(item)