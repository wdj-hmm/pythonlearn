#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from configparser import ConfigParser
import os
from common.handle_path import CONF_DIR


class Config(ConfigParser):
    def __init__(self, conf_file):
        super().__init__()
        self.read(conf_file, encoding='utf-8')


# conf = ConfigParser()
# conf.read(r'F:\pythonlearn\pylmb\conf\config.ini')

conf = Config(os.path.join(CONF_DIR, 'config.ini'))

# conf = Config(r'F:\pythonlearn\pylmb\conf\config.ini')
# collect_name = conf.get('logging','collect_name')
# collect_lever = conf.get()
# sh_lever = conf.get()
# file_name = conf.get()
