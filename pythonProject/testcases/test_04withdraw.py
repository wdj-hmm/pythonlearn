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
from common.handle_mysql import db1
from common.hand_re import replace_data
from testcases.fixture import Base_class


@ddt
class Test_Withdraw(unittest.TestCase,Base_class):
    excel = HandleExcel(os.path.join(DATA_DIR, 'apicase.xlsx'), 'withdraw')
    cases = excel.read_data()
    base_url = conf.get('env', 'base_url')
    # headers = eval(conf.get('head', 'head2'))
    db = db1

    @classmethod
    def setUpClass(cls) -> None:
        # url = cls.base_url + 'member/login'
        # paramas = {'mobile_phone': conf.get('test_data', 'mobile_phone'), 'pwd': conf.get('test_data', 'pwd')}
        # res = (requests.post(url=url, headers=cls.headers, json=paramas)).json()
        # token = jsonpath(res, '$..token')[0]
        # cls.headers['Authorization'] = 'Bearer ' + token
        # cls.member_id = jsonpath(res, '$..id')[0]
        cls.user_login()

    @list_data(cases)
    def test_withdraw(self, item):
        url = self.base_url + item['url']
        method = item['method'].lower()
        if '#member_id#' in item['data']:
            # item['data'] = item['data'].replace('#member_id#', str(self.member_id))
            item['data'] = replace_data(item['data'],Test_Withdraw)
        paramas = eval(item['data'])
        expected = eval(item['expected'])
        sql = 'SELECT leave_amount FROM futureloan.member WHERE mobile_phone ="{}"'.format(
            conf.get('test_data', 'mobile_phone'))
        start_mount = self.db.find_one(sql=sql)[0]
        print('提现前余额为：', start_mount)
        if self.headers["X-Lemonban-Media-Type"] == "lemonban.v3":
            paramas.update(self.par_sign)
        res = (requests.request(url=url, method=method, json=paramas, headers=self.headers)).json()

        # 取现后查询
        print("预期结果:", expected)
        print("实际结果:", res)
        end_mount = self.db.find_one(sql=sql)[0]
        print('提现后余额为：', end_mount)
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            if item['check_sql'] == 1:
                self.assertEqual(paramas.get('amount'),float(start_mount - end_mount))
        except AssertionError as e:
            Logger.error("用例--【{}】---执行失败".format(item['title']))
            Logger.exception(e)
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='失败')
            raise e
        else:
            Logger.info("用例--【{}】---执行成功".format(item['title']))
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='成功')
