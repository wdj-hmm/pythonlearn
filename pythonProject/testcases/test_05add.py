#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import unittest

import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from pythonProject.common.handle_excel import Handle_Excel
from pythonProject.common.handle_conf import conf
from pythonProject.common.handle_path import DATA_DIR
from pythonProject.common.hand_re import replace_data
from pythonProject.common.handle_log import Logger
from pythonProject.common.handle_mysql import db1
from pythonProject.testcases.fixture import Base_class


@ddt
class Test_add(unittest.TestCase,Base_class):
    '''
    这是前程贷项目添加测试类
    '''
    excel = Handle_Excel(os.path.join(DATA_DIR, 'apicase.xlsx'), 'add')
    cases = excel.read_data()
    base_url = conf.get('env', 'base_url')
    # headers = eval(conf.get('head', 'head2'))
    db = db1

    @classmethod
    def setUpClass(cls) -> None:
        # '''前置登录'''
        # url = cls.base_url + 'member/login'
        # paramas = {
        #     "mobile_phone": conf.get('test_data', 'mobile_phone'),
        #     "pwd": conf.get('test_data', 'pwd')
        # }
        # res = requests.post(url=url, headers=cls.headers, json=paramas)
        # resp = res.json()
        # token = jsonpath(resp, '$..token')[0]
        # # cls.headers = jsonpath(resp,'$..token_type')
        # cls.headers['Authorization'] = 'Bearer ' + token
        # cls.member_id = jsonpath(resp, '$..id')[0]
        # # print(cls.headers)
        cls.user_login()

    @list_data(cases)
    def test_add(self, item):
        url = self.base_url + '/loan/add'
        method = item['method'].lower()
        if '#member_id#' in item['data']:
            item['data'] = replace_data(item['data'], Test_add)

        paramas = eval(item['data'])
        excepeted = eval(item['expected'])
        sql = 'SELECT count(*) FROM futureloan.loan WHERE member_id={}'.format(self.member_id)

        if item['check_sql'] == 1:
            start_count = self.db.find_one(sql)[0]
            print('加载前的条数：', start_count)

        if self.headers["X-Lemonban-Media-Type"] == "lemonban.v3":
            paramas.update(self.par_sign)
        re = requests.request(method=method, url=url, json=paramas, headers=self.headers)
        res = re.json()
        if item['check_sql'] == 1:
            end_count = self.db.find_one(sql)[0]
            print('加载后的条数：', end_count, type(end_count))

        print("预期结果:", excepeted)
        print("实际结果:", res)
        try:
            self.assertEqual(excepeted['code'], res['code'])
            self.assertEqual(excepeted['msg'], res['msg'])
            if item['check_sql']:
                self.assertEqual(end_count - start_count, 1)
            # else:
            #     self.assertEqual(end_count - start_count, 0)
        except AssertionError as e:
            Logger.error("用例--【{}】---执行失败".format(item['title']))
            Logger.exception(e)
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='失败')
            raise e
        else:
            Logger.info("用例--【{}】---执行成功".format(item['title']))
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='成功')
