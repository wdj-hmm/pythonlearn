#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from unittestreport import ddt, list_data
from resiter1 import regsiter
from common.excel_fengzhuang import HandleExcel
from common.handle_log import logge,Logger


@ddt
class Test_regsiter(unittest.TestCase):
    excel = HandleExcel(r'F:\pythonlearn\Real_python_project\datas\cases.xlsx', 'regsiter')
    cases = excel.read_data()

    @list_data(cases)
    def test_regsiter(self, item):
        excepted = eval(item['expected'])
        data = eval(item['data'])
        res = regsiter(*data)
        try:
            self.assertEqual(excepted, res)
        except AssertionError as e:
            self.excel.write_data(row=item['id'] + 1, column=5, value='未通过')
            Logger.error('用例---[{}]----执行失败'.format(item["title"]))
            Logger.exception(e)
            raise e
        else:
            self.excel.write_data(row=item['id'] + 1, column=5, value='通过')
            Logger.info('用例---[{}]----执行通过'.format(item["title"]))
