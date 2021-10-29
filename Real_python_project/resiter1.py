#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def regsiter(username, password1, password2):
    users = [{'user': '王定金', "password": "123456"}]
    if not all([username, password1, password2]):
        return {"code": 0, "msg": "所有参数不能为空"}

    for user in users:
        if username == user['user']:
            return {"code": 0, "msg": "账户已存在"}

    else:
        if password1 != password2:
            return {"code": 0, "msg": "两次密码不一致"}
        else:
            if 6 <= len(password1) <= 18:
                users.append({'user': username, 'password': password1})
                return {"code": 1, "msg": "注册成功"}
            else:
                return {"code": 0, "msg": "密码必须在6-18位之间"}

