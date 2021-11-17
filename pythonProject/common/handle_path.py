#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''

此模块用来出来项目中的绝对路径

'''

import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 用例数据所在目录：
DATA_DIR = os.path.join(BASE_PATH, 'datas')
CONF_DIR = os.path.join(BASE_PATH, 'conf')
LOG_DIR = os.path.join(BASE_PATH, 'log')
REPORTS_DIR = os.path.join(BASE_PATH, 'reports')
CASES_DIR = os.path.join(BASE_PATH, 'testcases')
