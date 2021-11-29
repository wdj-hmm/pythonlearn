#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.handle_excel import Handle_Excel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import Logger
from common.hand_re import replace_data
from common.handle_mysql import db1
from testcases.fixture import Base_class


@ddt
class Test_audit(unittest.TestCase,Base_class):
    excel = Handle_Excel(os.path.join(DATA_DIR, 'apicase.xlsx'), 'audit')
    datas = excel.read_data()
    base_url = conf.get('env', 'base_url')
    db = db1

    @classmethod
    def setUpClass(cls) -> None:
        # '''类前置登录获取管理员token'''
        # url = cls.base_url + 'member/login'
        #
        # # ---------------管理员用户登录-----------------
        # paramas1 = {
        #     "mobile_phone": conf.get('test_data', 'admin_moblie'),
        #     "pwd": conf.get('test_data', 'admin_pwd')
        # }
        # headers = eval(conf.get('head', 'head2'))
        # respounse = requests.post(url=url, json=paramas1, headers=headers)
        # res = respounse.json()
        # token_admin = jsonpath(res, '$..token')[0]
        # headers['Authorization'] = 'Bearer ' + token_admin
        # cls.admin_headers = headers
        # cls.admin_member_id = jsonpath(res, '$..id')[0]
        # # ----------------普通用户登录------------------
        # paramas = {
        #     "mobile_phone": conf.get('test_data', 'mobile_phone'),
        #     "pwd": conf.get('test_data', 'pwd')
        # }
        # headers2 = eval(conf.get('head', 'head2'))
        # res = (requests.post(url=url, json=paramas, headers=headers2)).json()
        # token = jsonpath(res, '$..token')[0]
        # headers2['Authorization'] = 'Bearer ' + token
        # cls.headers = headers2
        # cls.member_id = jsonpath(res, '$..id')[0]
        cls.admin_login()
        cls.user_login()

    def setUp(self) -> None:
        # url = self.base_url + '/loan/add'
        # paramas3 = {"member_id": self.member_id,
        #             "title": "老王给你们面子借钱给你",
        #             "amount": 100,
        #             "loan_rate": 12.0,
        #             "loan_term": 3,
        #             "loan_date_type": 1,
        #             "bidding_days": 5}
        # res = (requests.post(url=url, json=paramas3, headers=self.headers)).json()
        # Test_audit.loan_id = jsonpath(res, '$..id')[0]
        # # setattr(Test_audit, 'loan_id', jsonpath(res, '$..id')[0])
        self.add_project()

    @list_data(datas)
    def test_audit(self, item):
        # print("执行当前用例，类属性中的loan_id",self.loan_id)
        url = self.base_url + item['url']
        method = item['method'].lower()

        item['data'] = replace_data(item['data'], Test_audit)
        paramas = eval(item['data'])
        expected = eval(item['expected'])
        if self.admin_headers["X-Lemonban-Media-Type"] == "lemonban.v3":
            paramas.update(self.admin_par_sign)
        response = requests.request(url=url, method=method, json=paramas, headers=self.admin_headers)
        res = response.json()
        # 判断是否通过的用例，如果是保存为通过的项目id pass_loan_id
        if res['msg'] == 'OK' and item['title'] == '审核通过':
            # setattr(Test_audit, 'pass_loan_id', self.loan_id)
            Test_audit.pass_loan_id = paramas['loan_id']
        print("预期结果:", expected)
        print("实际结果:", res)

        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            if item['check_sql']:
                sql = item['check_sql'].format(self.loan_id)
                status = self.db.find_one(sql)[0]
                print("数据库中的状态值为：", status)
                self.assertEqual(expected['status'], status)
        except AssertionError as e:
            Logger.error("用例--【{}】---执行失败".format(item['title']))
            Logger.exception(e)
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='失败')
            raise e
        else:
            Logger.info("用例--【{}】---执行成功".format(item['title']))
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='成功')


