#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
'''
日志分两类：收集器，输出
'''
# 创建日志收集器
log = logging.getLogger('AutoLogging')
# 设置收集器获取的日志等级
log.setLevel('INFO')

# # 输出：1、输出到文件夹
# fh = logging.FileHandler('AutoLogging.log',encoding="utf-8")
# fh.setLevel("ERROR")
# log.addHandler(fh)

# 输出：2、输出到控制台
sh = logging.StreamHandler()
sh.setLevel("INFO")
log.addHandler(sh)

#先设置一个格式对象模板，然后将输出控制台的格式设置为模板
formats = '%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s:%(message)s'
# simple_format = '[task_id:%(name)s][%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
# log_format = logging.Formatter('%(funcName)s :[%(levelname)s] ：%(asctime)s:%(message)s')
log_format = logging.Formatter(formats)

sh.setFormatter(log_format)

# fh.setFormatter(log_format)


log.debug("-----------debug---------")
log.info("-----------info---------")
log.warning("-----------warning---------")
log.error("-----------error---------")
log.critical("-----------critical---------")