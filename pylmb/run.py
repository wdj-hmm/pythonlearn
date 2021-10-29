#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

import unittestreport

s = unittest.defaultTestLoader.discover(r'F:\pythonlearn\pylmb')
run = unittestreport.TestRunner(s)
run.run()
run.dingtalk_notice(key='自动化')