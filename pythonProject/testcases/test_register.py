#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
import requests
import random
from unittestreport import ddt, list_data
from common.excel_fengzhuang import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import logge, Logger
from common.handle_mysql import db1


@ddt
class TestRegister(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, 'apicase.xlsx'), 'register')
    cases = excel.read_data()
    base_url = conf.get('env', 'base_url')
    headers = eval(conf.get('head', 'head2'))
    db1 = db1

    @list_data(cases)
    def test_register(self, item):
        #     准备用例数据
        url = self.base_url + item['url']
        if '#mobile_phone#' in item['data']:
            item['data'] = item['data'].replace('#mobile_phone#', self.randow_mobile())
        params = eval(item['data'])
        # 获取请求方法并转换为小写
        method = item['method'].lower()
        expected = eval(item['expected'])
        #       eval 将字符串转化为字典
        #     请求接口,获取返回数据
        response = requests.request(method=method, url=url, json=params, headers=self.headers)
        res = response.json()

        if res['msg'] == 'OK':
            sql = "SELECT COUNT(*) FROM futureloan.member WHERE mobile_phone = '{}'".format(item['data'][0])
            self.db1.execute_sql(sql=sql)
            sqlr = self.db1.get_data()[0][0]
            print(sqlr)


        #     第三部:断言
        print("预期结果:", expected)
        print("实际结果:", res)
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            # if res['msg'] == 'OK':
            #     self.assertEqual(sqlr, 1)
            # # else:
            #     self.assertEqual(sqlr, 0)

        except AssertionError as e:
            Logger.error("用例--【{}】---执行失败".format(item['title']))
            Logger.exception(e)
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='失败')
            raise e
        else:
            Logger.info("用例--【{}】---执行成功".format(item['title']))
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='成功')

    def randow_mobile(self):
        mobile_phone = str(random.randint(13300000000, 13399999999))
        return mobile_phone
