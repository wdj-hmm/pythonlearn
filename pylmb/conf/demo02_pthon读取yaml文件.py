#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml

c = r'F:\pythonlearn\newweb\data\loginCase.yaml'
with open(c, 'r', encoding='utf-8') as f:
    res = yaml.load(f, Loader=yaml.Loader)

print(res,type(res))
