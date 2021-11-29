#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import unittest

import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data

from common.handle_conf import conf
from common.handle_excel import Handle_Excel
from common.handle_path import DATA_DIR
from common.handle_log import Logger
from common.hand_re import replace_data
from common.handle_mysql import db1
from testcases.fixture import Base_class


@ddt
class Test_invest(unittest.TestCase, Base_class):
    excel = Handle_Excel(os.path.join(DATA_DIR, 'apicase.xlsx'), 'invest')
    datas = excel.read_data()
    db = db1

    @classmethod
    def setUpClass(cls) -> None:
        cls.admin_login()
        cls.user_login()
        cls.add_project()
        cls.audit_project()

    @list_data(datas)
    def test_invest(self, item):
        pass
        url = self.base_url + item['url']
        method = item['method']
        item['data'] = replace_data(item['data'], Test_invest)
        paramas = eval(item['data'])
        expected = eval(item['expected'])
        # 投资前查询数据库
        sql1 = 'SELECT leave_amount FROM futureloan.member WHERE id ="{}"'.format(self.member_id)
        sql2 = 'SELECT id from futureloan.invest where member_id ="{}"'.format(self.member_id)
        sql3 = 'SELECT id FROM futureloan.financelog WHERE pay_member_id ={}'.format(self.member_id)
        if item['check_sql']:
            start_money = self.db.find_one(sql1)[0]
            start_invest = self.db.find_count(sql2)
            start_financelog = self.db.find_count(sql3)
        if self.headers["X-Lemonban-Media-Type"] == "lemonban.v3":
            paramas.update(self.par_sign)
        response = requests.request(url=url, method=method, json=paramas, headers=self.headers)
        res = response.json()
        # 投资后查询数据库
        if item['check_sql']:
            end_money = self.db.find_one(sql1)[0]
            end_invest = self.db.find_count(sql2)
            end_financelog = self.db.find_count(sql3)

        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertIn(expected['msg'], res['msg'])
            if item['check_sql']:
                self.assertEqual(paramas['amount'], float(start_money - end_money))
                self.assertEqual(1, end_invest - start_invest)
                self.assertEqual(1, end_financelog - start_financelog)
        except AssertionError as e:
            Logger.error("用例--【{}】---执行失败".format(item['title']))
            Logger.exception(e)
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='失败')
            raise e
        else:
            Logger.info("用例--【{}】---执行成功".format(item['title']))
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='成功')
