#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from time import time
from jsonpath import jsonpath

from pythonProject.common.handle_conf import conf
from pythonProject.common.handle_sign import Handle_sign


class Base_class:
    base_url = conf.get('env', 'base_url')

    @classmethod
    def admin_login(cls):
        '''类前置登录获取管理员token'''
        url = cls.base_url + 'member/login'
        # ---------------管理员用户登录-----------------
        paramas1 = {
            "mobile_phone": conf.get('test_data', 'admin_moblie'),
            "pwd": conf.get('test_data', 'admin_pwd')
        }
        headers = eval(conf.get('head', 'head3'))

        respounse = requests.post(url=url, json=paramas1, headers=headers)
        res = respounse.json()
        token_admin = jsonpath(res, '$..token')[0]
        headers['Authorization'] = 'Bearer ' + token_admin
        cls.admin_token = token_admin
        if headers["X-Lemonban-Media-Type"] == "lemonban.v3":
            cls.admin_par_sign = Handle_sign.generate_sign(cls.admin_token)
        cls.admin_headers = headers
        cls.admin_member_id = jsonpath(res, '$..id')[0]

    @classmethod
    def user_login(cls):
        # ----------------普通用户登录------------------
        url = cls.base_url + 'member/login'
        paramas = {
            "mobile_phone": conf.get('test_data', 'mobile_phone'),
            "pwd": conf.get('test_data', 'pwd')
        }
        headers2 = eval(conf.get('head', 'head3'))
        res = (requests.post(url=url, json=paramas, headers=headers2)).json()
        token = jsonpath(res, '$..token')[0]
        headers2['Authorization'] = 'Bearer ' + token
        cls.token = token
        if headers2["X-Lemonban-Media-Type"] == "lemonban.v3":
            cls.par_sign = Handle_sign.generate_sign(cls.token)
            print(cls.par_sign)
        cls.headers = headers2
        cls.member_id = jsonpath(res, '$..id')[0]

    @classmethod
    def add_project(cls):
        # ----------------普通用户创建项目---------------
        url = cls.base_url + '/loan/add'
        paramas3 = {"member_id": cls.member_id,
                    "title": "老王给你们面子借钱给你",
                    "amount": 2000,
                    "loan_rate": 12.0,
                    "loan_term": 3,
                    "loan_date_type": 1,
                    "bidding_days": 5}
        if cls.headers['X-Lemonban-Media-Type'] == 'lemonban.v3':
            par_sign = Handle_sign.generate_sign(cls.token)
            paramas3.update(par_sign)
        res = (requests.post(url=url, json=paramas3, headers=cls.headers)).json()
        cls.loan_id = jsonpath(res, '$..id')[0]

    @classmethod
    def audit_project(cls):
        '''管理员审核项目'''
        url = cls.base_url + '/loan/audit'
        paramas = {"loan_id": cls.loan_id, "approved_or_not": True}
        if cls.admin_headers['X-Lemonban-Media-Type'] == 'lemonban.v3':
            # par_sign = Handle_sign.generate_sign(cls.token)
            paramas.update(cls.admin_par_sign)
        res = requests.patch(url=url, json=paramas, headers=cls.admin_headers)


if __name__ == '__main__':
    c = Base_class()
    c.user_login()
    c.add_project()
