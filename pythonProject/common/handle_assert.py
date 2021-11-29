#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Handle_Assert():

    def assertDictIn(self, expected, res):
        '''字典成员运算的逻辑'''
        for k, v in expected.items:
            if res.get(k) == v:
                pass
            else:
                raise AssertionError("{} not in {}".format(expected, res))
