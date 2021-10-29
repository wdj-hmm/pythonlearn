#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from configparser import ConfigParser

class Config(ConfigParser):
    def __init__(self,conf_file):
        super().__init__()
        self.read(conf_file,encoding='utf-8')

# conf = ConfigParser()
# conf.read(r'F:\pythonlearn\pylmb\conf\logging.ini')

conf = Config(r'F:\pythonlearn\Real_python_project\conf\logging.ini')

# conf = Config(r'F:\pythonlearn\pylmb\conf\logging.ini')
# collect_name = conf.get('logging','collect_name')
# collect_lever = conf.get()
# sh_lever = conf.get()
# file_name = conf.get()