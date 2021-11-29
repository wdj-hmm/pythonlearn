#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest
import unittestreport
import HTMLTestRunner
from common.handle_path import CASES_DIR, REPORTS_DIR
from unittestreport.core.sendEmail import SendEmail

class run:

    def main(self):
        suit = unittest.defaultTestLoader.discover(CASES_DIR)
        res = unittestreport.TestRunner(suit, report_dir=REPORTS_DIR)
        res.run()
        res.dingtalk_notice()
        res.send_email(host='smtp.qq.com',
                       port=465,
                       user='542763903@qq.com',
                       password='kdwvkibxdwkzbebb',
                       to_addrs='dingjinwang@melot.cn',
                       is_file=True)

# 拓展自己控制邮件标题内容
#         em = SendEmail(host='smtp.qq.com',user='542763903@qq.com',password='kdwvkibxdwkzbebb')
#         em.send_email(subject="你猜这是啥", content='猜猜我是谁', filename={}, to_addrs='dingjinwang@melot.cn')

if __name__ == '__main__':
    run = run().main()

