#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest
import unittestreport

suit = unittest.defaultTestLoader.discover(r'F:\pythonlearn\Real_python_project\testcases')
print(suit)
res = unittestreport.TestRunner(suit)
res.run()
res.dingtalk_notice()
