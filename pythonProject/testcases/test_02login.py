#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
import requests
from unittestreport import ddt, list_data
from common.excel_fengzhuang import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import logge, Logger
from common.handle_assert import Handle_Assert
from common.hand_re import replace_data

@ddt
class Test_Login(unittest.TestCase):
    excel1 = HandleExcel(os.path.join(DATA_DIR, 'apicase.xlsx'), 'login')
    cases = excel1.read_data()
    base_url = conf.get('env', 'base_url')
    headers = eval(conf.get('head', 'head2'))
    c = Handle_Assert()

    @list_data(cases)
    def test_login(self, item):
        url = self.base_url + item['url']
        method = item['method'].lower()
        item['data'] = replace_data(item['data'],Test_Login)
        paramas =eval(item['data'])
        response = requests.request(method=method, url=url, headers=self.headers,json=paramas)
        res = response.json()
        excepted = eval(item['expected'])
        print("预期结果:", excepted)
        print("实际结果:", res)
        try:
            self.assertEqual(excepted['code'], res['code'])
            self.assertEqual(excepted['msg'], res['msg'])
            # 此处是调用自己封装的assert方法，判断key,value是否在预期结果中
            # self.c.assertDictIn(excepted,res)
        except AssertionError as e:
            Logger.error("用例--【{}】---执行失败".format(item['title']))
            Logger.exception(e)
            self.excel1.write_data(row=item['case_id'] + 1, column=8, value='失败')
            raise e
        else:
            Logger.info("用例--【{}】---执行成功".format(item['title']))
            self.excel1.write_data(row=item['case_id'] + 1, column=8, value='成功')
