#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.excel_fengzhuang import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import Logger

@ddt
class Test_Withdraw(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, 'apicase.xlsx'), 'withdraw')
    cases = excel.read_data()
    base_url = conf.get('env', 'base_url')
    headers = eval(conf.get('head', 'head2'))

    @classmethod
    def setUpClass(cls) -> None:
        url = cls.base_url + 'member/login'
        paramas = {'mobile_phone': conf.get('test_data', 'mobile_phone'), 'pwd': conf.get('test_data', 'pwd')}
        res = (requests.post(url=url, headers=cls.headers, json=paramas)).json()
        token = jsonpath(res, '$..token')[0]
        cls.headers['Authorization'] = 'Bearer ' + token
        cls.member_id = jsonpath(res, '$..id')[0]

    @list_data(cases)
    def test_withdraw(self, item):
        url = self.base_url + item['url']
        method = item['method'].lower()
        if '#member_id#' in item['data']:
            item['data'] = item['data'].replace('#member_id#', str(self.member_id))
        paramas = eval(item['data'])
        expected = eval(item['expected'])
        res = (requests.request(url=url, method=method, json=paramas,headers=self.headers)).json()
        print("预期结果:", expected)
        print("实际结果:", res)
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
        except AssertionError as e:
            Logger.error("用例--【{}】---执行失败".format(item['title']))
            Logger.exception(e)
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='失败')
            raise e
        else:
            pass
            Logger.info("用例--【{}】---执行成功".format(item['title']))
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='成功')




