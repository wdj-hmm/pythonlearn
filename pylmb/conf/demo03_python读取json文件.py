#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

with open('data.json', 'r', encoding="utf-8") as f:
    res = json.load(f)
    resd = res['logging']['sh_lever']
print(res, type(res))
print(resd, type(resd))

'''
json 文件中字典叫对象，列表叫数组
python中  NULL   =   json中   null
python中  False   =   json中  false
python中  Ture   =   json中  ture
'''
# --------------------python转json使用json.dumps--------------------------
dic = {"aa": None, "bb": 'python', "cc": True, "dd": [11, 22, 33]}
res = json.dumps(dic)
print(res)
# --------------------json转python使用json.loads--------------------------
s_json = '{"aa":null,"bb":"python","cc":true,"dd":[11,22,33]}'
resr = json.loads(s_json)
print(resr)
