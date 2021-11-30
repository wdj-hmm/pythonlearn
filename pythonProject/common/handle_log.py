#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import time
import colorlog
from pythonProject.common.handle_conf import conf
from pythonProject.common.handle_path import LOG_DIR

colorlog_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',

}


def create_log(collect_name='my_log', collect_lever='DEBUG', sh_lever='DEBUG', file_name='log.log'):
    # 生成日志收集器
    logger = logging.getLogger(collect_name)
    logger.setLevel(collect_lever)

    # 输出到控制台
    log_console = logging.StreamHandler()
    log_console.setLevel(sh_lever)

    # 输出到日志文件
    log_file = logging.FileHandler(file_name, encoding='utf-8')
    log_file.setLevel(sh_lever)

    # 设置日志格式
    # classic_formats = '%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s:%(message)s'
    # log_format = logging.Formatter(classic_formats)
    log_format = colorlog.ColoredFormatter(
        '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s',
        log_colors=colorlog_config)

    # 设置输出方式的格式
    log_console.setFormatter(log_format)
    log_file.setFormatter(log_format)

    # 往加载器塞数据
    logger.addHandler(log_console)
    logger.addHandler(log_file)

    return logger

    # # 移除处理器
    # logger.removeHandler(log_console)
    # logger.removeHandler(log_file)


# 解决程序中避免重复创建日志收集器，日志重复输出，我们直接创建唯一一个日志收集器，模块直接导用该日志收集器对象

# cp = ConfigParser()
# cp.read(r'F:\pythonlearn\pylmb\conf\config.ini', encoding="utf-8")
# res = cp.get('logging')

logge = create_log(
    collect_name=conf.get('logging', 'collect_name'),
    collect_lever=conf.get('logging', 'collect_lever'),
    sh_lever=conf.get('logging', 'sh_lever'),
    file_name=os.path.join(LOG_DIR, conf.get('logging', 'file_name')))

# Method2
BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# 日志文件路径
LOG_PATH = os.path.join(BASE_PATH, "log")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


class Logger():

    def __init__(self):
        self.logname = os.path.join(LOG_PATH, "{}.log".format(time.strftime("%Y-%m-%d")))
        self.logger = logging.getLogger("log")
        self.logger.setLevel(logging.DEBUG)

        # self.formater = logging.Formatter(
        #     '[%(asctime)s][%(filename)s %(lineno)d][%(levelname)s]: %(message)s')
        self.formater = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s',
            log_colors=colorlog_config)

        self.filelogger = logging.FileHandler(self.logname, mode='a', encoding="UTF-8")
        self.console = logging.StreamHandler()
        self.console.setLevel(logging.DEBUG)
        self.filelogger.setLevel(logging.DEBUG)
        self.filelogger.setFormatter(self.formater)
        self.console.setFormatter(self.formater)
        self.logger.addHandler(self.filelogger)
        self.logger.addHandler(self.console)


Logger = Logger().logger
