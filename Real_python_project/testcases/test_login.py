#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from unittestreport import ddt, list_data
from login_func import login_check
from common.excel_fengzhuang import HandleExcel
from common.handle_log import logge,Logger


@ddt
class TestLogin(unittest.TestCase):
    excel = HandleExcel(r'F:\pythonlearn\Real_python_project\datas\cases.xlsx', 'login')
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
            self.excel.write_data(row=item['id'] + 1, column=5, value="未通过")
            Logger.error('用例---[{}]----执行失败'.format(item["title"]))
            Logger.error(e)
            raise e
        else:
            print("用例执行通过")
            self.excel.write_data(row=item['id'] + 1, column=5, value="通过")
            Logger.info('用例---[{}]----执行成功'.format(item["title"]))
