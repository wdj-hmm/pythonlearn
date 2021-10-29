#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from unittestreport import ddt, list_data
from pylmb.login_func import login_check
import openpyxl
from pylmb.base_fengzhuang.excel_fengzhuang import HandleExcel
from pylmb.base_fengzhuang.handle_log import logge





@ddt
class TestLogin(unittest.TestCase):
    excel = HandleExcel(r'F:\pythonlearn\pylmb\cases.xlsx', 'login')
    cases = excel.read_data()

    @list_data(cases)
    def test_login(self, item):
        expected = eval(item['expected'])
        params = eval(item['data'])
        res = login_check(**params)
        try:
            self.assertEqual(expected, res)
        except AssertionError as e:
            print("用例执行未通过")
            self.excel.write_data(row=item['id']+1, column=5, value="未通过")
            logge.error('用例---[{}]----执行失败'.format(item["title"]))
            logge.error(e)
            raise e
        else:
            print("用例执行通过")
            self.excel.write_data(row=item['id']+1, column=5, value="通过")
            logge.info('用例---[{}]----执行成功'.format(item["title"]))