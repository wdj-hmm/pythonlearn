#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql
from common.handle_conf import conf


class Operation_mysql:
    """
    pymysql提供的方法如下：
    1. 建立数据库连接 conn = pymysql.connect()
    2. 从连接建立操作游标 cur = conn.cursor()
    3. 使用游标执行sql（读/写） cur.execute(sql)
    4. 获取结果（读）/ 提交更改（写） cur.fetchall() / conn.commit()
    5. 关闭游标及连接 cur.close();conn.close()
    """

    def __init__(self, host, port, user, password, *args, **kwargs):
        # 一、连接数据库
        self.connection = pymysql.connect(host=host,
                                          port=port,
                                          user=user,
                                          password=password,
                                          charset="utf8",
                                          *args, **kwargs
                                          )
        # 2、创建游标对象
        self.cur = self.connection.cursor()
        # self.cur = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        # with self.connection as cur:
        #     cur.execute()

    '''
    默认都是返回元组的数据类型，看起来不太直观，因此，在实例化时可以将游标设置成如下这样，就可以返回字典类型的数据
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    '''

    def execute_sql(self, sql):
        try:
            self.cur.execute(sql)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
        # finally:
        #     self.cur.close()

    def get_data(self):
        """
        查询操作：
              使用cur.execute(), 执行数据库查询后无返回的是影响的行数，而非查询结果。我们要使用cur.fetchone()/cur.fetchmany()/cur.fetchall()来获取查询结果
              cur.fetchone(): 获取一条数据（同时获取的数据会从结果集删除），返回元组
              cur.fetchmany(3): 获取多条数据，返回嵌套元组
              cur.fetchall(): 获取所有数据，返回嵌套元组
            """
        # datas = self.cur.fetchone()
        # datas = self.cur.fetchmany()
        datas = self.cur.fetchall()
        return datas

    # def close_mysql(self):
    def __del__(self):
        self.cur.close()
        self.connection.close()


#     --------------------------------------------------柠檬班方法---------------------------------------------------------------
    def find_all(self,sql):
        self.cur.execute(sql)
        res = self.cur.fetchall()
        # self.cur.close()
        return res

    def find_one(self,sql):
        # cur = self.connection.cursor()
        # cur.execute(sql)
        # res = cur.fetchone()
        # cur.close()
        # return res
        with self.connection as cur:
            res = cur.execute(sql)
            resp =cur.fetchone()
        cur.close()
        return resp


    def find_count(self,sql):
        with self.connection as cur:
            res = cur.execute(sql)
        cur.close()
        return res


db1 = Operation_mysql(host=conf.get('mysql', 'host'),
                          port=conf.getint('mysql', 'port'),
                          user=conf.get('mysql', 'user'),
                          password=conf.get('mysql', 'password')
                          )


# if __name__ == '__main__':
#     # sql = "SELECT * FROM futureloan.member WHERE mobile_phone ='13388285002';"
#     sql = "SELECT leave_amount FROM futureloan.member WHERE mobile_phone ='13388285002';"
# #
# # host = conf.get('mysql', 'host'),
# # port = conf.getint('mysql', 'port'),
# # user = conf.get('mysql', 'user'),
# # password = conf.get('mysql', 'password'),
# # charset = "utf8"
#     db1 = Operation_mysql(host=conf.get('mysql', 'host'),
#                         port=conf.getint('mysql', 'port'),
#                         user=conf.get('mysql', 'user'),
#                         password=conf.get('mysql', 'password')
#                        )
#     db1.execute_sql(sql)
#     c = db1.get_data()
#     d = c[0]
#     e =d[0]
#     print(c)
#     print(d)
#     print(e,type(e))
#     # s.close_mysql()
#     del db1

# # 3、执行sql
# res = cur.execute(sql)
# # execute的结果是展示查询到了几条数据
# # print(res)
#
# # 4、获取结果((),(),())
#
# data = cur.fetchall()
# print(data)
#
# # 提交事务，涉及增删改，执行sql完事务才会生效
# db.commit()
#
# -----------------------------快捷创建游标(自动提交事务)-----------------------------------(该版本pymysql无上下文功能)
# conn.__enter__()
# with conn as cur:
#     sql = "SELECT leave_amount FROM futureloan.member WHERE mobile_phone ='13388285002'"
#     cur.execute(sql)
#
# # 4.关闭游标
# cur.close()
# # 5.断开连接
# db.close()
