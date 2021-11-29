#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
from time import time

import rsa


class Handle_sign():
    pub_str = """
    -----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQENQujkLfZfc5Tu9Z1LprzedE
    O3F7gs+7bzrgPsMl29LX8UoPYvIG8C604CprBQ4FkfnJpnhWu2lvUB0WZyLq6sBr
    tuPorOc42+gLnFfyhJAwdZB6SqWfDg7bW+jNe5Ki1DtU7z8uF6Gx+blEMGo8Dg+S
    kKlZFc8Br7SHtbL2tQIDAQAB
    -----END PUBLIC KEY-----
    """

    @classmethod
    def encrypt(cls, msg):
        '''
        :param msg: 待加密字符串或字节
        :return: 密文
        '''

        msg = msg.encode('utf-8')
        pub_key = cls.pub_str.encode('utf-8')
        public_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)  # 创建rsa加密对象
        cryto_msg = rsa.encrypt(msg, public_key_obj)  # 生成加密文本
        cipher_base64 = base64.b64encode(cryto_msg)  # 将加密文本转化为base64 编码
        return cipher_base64.decode()  # 将字节类型的base64 编码转化为字符串类型

    # @classmethod缺少解密key
    # def decrypt(cls, msg):
    #     msg = base64.b64decode(msg)
    #     decrtpt_msg = rsa.decrypt(msg,)

    @classmethod
    def generate_sign(cls, token, timestamp=None):
        timestamp = timestamp or int(time())  # 获取当前时间的时间戳
        prefix_50_token = token[:50]  # 获取token前50位
        message = prefix_50_token + str(timestamp)
        sign = cls.encrypt(message)
        return {"timestamp": timestamp, "sign": sign}


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzUxMiJ9.eyJtZW1iZXJfaWQiOjIwOTgxNywiZXhwIjoxNjM3OTIwMTE0fQ.RlpBRPtvjpHbsX6GJxB3J5_8coeWMYuWqsBEpiwd7hfQF0JcY5o04WBiRxYGcxvGhmjs05PkJQZccgXj_it63g"
    crypt_info = Handle_sign.generate_sign(token)
    print(crypt_info)
