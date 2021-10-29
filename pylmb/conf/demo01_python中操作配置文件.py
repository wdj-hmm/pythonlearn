#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from configparser import ConfigParser

# 创建一个配置解析器对象
cp = ConfigParser()
# 读取配置文件中的内容并放到配置解析器
cp.read('logging.ini', encoding='utf-8')
# 读取一：从配置解析器中去获取内容，内容都会当做字符串
res = cp.get('logging', 'level')
# 读取二:getint:读取数值类型的数据
# res2= cp.getint()
# 读取三:getint:读取布尔类型的数据
# res3 = cp.getboolean()
# 读取四:getint:读取浮点类型的数据
# res4 = cp.getfloat()
print(res)

# 配置文件写入
cp.set('logging', 'sh_lever', 'DEBUG')
cp.write(fp=open('logging.ini','w',encoding='utf-8'))
