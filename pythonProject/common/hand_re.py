#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pythonProject.common.handle_conf import conf


class poy:
    id = 5
    name = 'wdj'


s = '{"id":"#id#","name":"#name#"}'


def replace_data(data, cls, method='#(.+?)#'):
    '''
    :param data: 要进行替换的用例数据（字符串）
    :param cls: 测试类
    :param method: 正则方法
    :return:
    '''
    while re.search(method, data):
        res = re.search(method, data)
        item = res.group()
        attrs = res.group(1)
        try:
            value = getattr(cls, attrs)
        except AttributeError as e:
            # 从配置文件读取数据
            value = conf.get('test_data', attrs)
        data = data.replace(item, str(value))
    return data


if __name__ == '__main__':
    # re = handle_re()
    data = replace_data(s, poy)
    print(data)

s = {"member_id": "","title":"老王给你们面子借钱给你","amount":2000,"loan_rate":12.0,"loan_term":3,"loan_date_type":1,"bidding_days":5}
