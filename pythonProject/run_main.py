#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest
import unittestreport
from common.handle_path import CASES_DIR, REPORTS_DIR

suit = unittest.defaultTestLoader.discover(CASES_DIR)

res = unittestreport.TestRunner(suit, report_dir=REPORTS_DIR)
res.run()
res.dingtalk_notice()
