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
from common.handle_log import Logger, logge
from common.handle_mysql import db1

'''
用例级别的前置: setup
测试类级别前置：setUpClass
'''


@ddt
class Test_Recharge(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, 'apicase.xlsx'), 'recharge')
    cases = excel.read_data()
    headers = eval(conf.get('head', 'head2'))
    base_url = conf.get('env', 'base_url')
    db1 = db1
    @classmethod
    def setUpClass(cls) -> None:
        """用例类的前置方法，等去提取token"""
        url = conf.get('env', 'base_url') + '/member/login'
        headers = cls.headers
        paramas = {'mobile_phone': conf.get('test_data', 'mobile_phone'), 'pwd': conf.get('test_data', 'pwd')}
        response = requests.post(url=url, headers=headers, json=paramas)
        res = response.json()
        # jsonpath取出来的值是一个列表，[0]索引取值
        token = jsonpath(res, '$..token')[0]
        # 方法一：更新字典
        # cls.headers.update({'Authorization': 'Bearer {}'.format(token)})
        # 方法二 与上面类似，有则更新，无则添加
        cls.headers['Authorization'] = 'Bearer ' + token

        # 从登录中获取充值接口的member_id,避免登录账号和充值接口member_id不一致
        cls.member_id = jsonpath(res, '$..id')[0]

    @list_data(cases)
    def test_recharge(self, item):

        url = self.base_url + item['url']
        method = item['method'].lower()
        # *************************************************动态处理参数***************************************************
        # 动态处理需要进行替换的参数，使用字符串的replace方法
        if '#member_id#' in item['data']:
            item['data'] = item['data'].replace('#member_id#', str(self.member_id))
        # **************************************************************************************************************
        paramas = eval(item['data'])
        # sql = item['check_sql'.format(conf.get('test_data', 'mobile_phone'))]
        sql = "SELECT leave_amount FROM futureloan.member WHERE mobile_phone ='{}'".format(
            conf.get('test_data', 'mobile_phone'))
        print(sql)

        self.db1.execute_sql(sql)
        start_amounts = self.db1.get_data()[0][0]
        # print(start_amounts,type(start_amounts))
        print('查询前余额为：' + str(start_amounts))

        response = requests.request(method=method, url=url, headers=self.headers, json=paramas)
        res = response.json()
        excepeted = eval(item['expected'])
        self.db1.execute_sql(sql)
        end_amounts = self.db1.get_data()[0][0]
        print('查询后余额为：' + str(end_amounts))
        print("预期结果:", excepeted)
        print("实际结果:", res)
        try:
            self.assertEqual(excepeted['code'], res['code'])
            self.assertEqual(excepeted['msg'], res['msg'])
            if res['msg'] == 'OK':
                # 充值成功，校验充值金额
                self.assertEqual(float(end_amounts - start_amounts), paramas['amount'])
            else:
                # 充值失败，余额变化为0
                self.assertEqual(end_amounts - start_amounts, 0)
        except AssertionError as e:

            Logger.error("用例--【{}】---执行失败".format(item['title']))
            Logger.exception(e)
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='失败')
            raise e
        else:
            pass
            Logger.info("用例--【{}】---执行成功".format(item['title']))
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='成功')
