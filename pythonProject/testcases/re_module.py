#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

str1 = 'as656685631aa#id#,c2#data#,._@$%#^'

# {n}表示一个字符出现n次
r1 = re.findall('\d', str1)
# print(r1)

'''
字符串边界
        ^表示字符串开头（开始位置）
        $表示字符串结尾（终止位置）
        
单词边界
       \b表示单词边界
       \B表示非单词边界
'''
s = "0123saiud456oi@789++c"
res = re.findall('^0123', s)
print(res)


# ---------------------|-------------------------表示多个匹配规则，或的意思



# findall匹配所有符合规则的数据，列表返回

# search匹配并返回第一个符合规则的匹配对象

# group()提取匹配对象中的内容





def finbo(n):
    a = b =1
    for i in range(n):
        yield a
        a,b = b,a+b

c = finbo(5)
for i in c:
    print(i)