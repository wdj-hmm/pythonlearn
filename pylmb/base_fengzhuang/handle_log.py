#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging


def create_log(collect_name='my_log', collect_lever='DEBUG',sh_lever='DEBUG',file_name='log.log'):
    logger = logging.getLogger(collect_name)
    logger.setLevel(collect_lever)
    # 输出到控制台
    log_console = logging.StreamHandler()
    log_console.setLevel(sh_lever)


    # 输出到日志文件
    log_file = logging.FileHandler(file_name, encoding='utf-8')
    log_file.setLevel(sh_lever)



    # 设置日志格式
    classic_formats = '%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s:%(message)s'
    log_format = logging.Formatter(classic_formats)

    log_console.setFormatter(log_format)
    log_file.setFormatter(log_format)

    # 往加载器塞数据
    logger.addHandler(log_console)
    logger.addHandler(log_file)


    return logger

    # # 移除处理器
    # logger.removeHandler(log_console)
    # logger.removeHandler(log_file)



logge = create_log()