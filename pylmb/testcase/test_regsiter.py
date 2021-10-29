#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from unittestreport import ddt, list_data
from pylmb.resiter1 import regsiter
from pylmb.base_fengzhuang.excel_fengzhuang import HandleExcel
from pylmb.base_fengzhuang.handle_log import logge


@ddt
class Test_regsiter(unittest.TestCase):
    excel = HandleExcel(r'F:\pythonlearn\pylmb\cases.xlsx', 'regsiter')
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
            logge.error('用例---[{}]----执行失败'.format(item["title"]))
            logge.exception(e)
            raise e
        else:
            self.excel.write_data(row=item['id'] + 1, column=5, value='通过')
            logge.info('用例---[{}]----执行通过'.format(item["title"]))
