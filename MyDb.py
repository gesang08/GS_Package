#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

"""
实现操作数据库的类，可将从数据库获得的以字段为键，以字段内容为值的存储格式数据；
"""

import MySQLdb
import MySQLdb.cursors
from CONST_DEFINE import *


class Database(object):
    """
    封装数据库操作类
    """
    # 注，python的self等于其它语言的this
    def __init__(self, log=None, dbhost=None, dbname=None, user=None, password=None, port=None, charset=None):
        self._logger = log
        # 这里的None相当于其它语言的NULL
        self._dbhost = SERVER_IP if dbhost is None else dbhost
        self._dbname = DB if dbname is None else dbname
        self._user = USER if user is None else user
        self._password = PASSWORD if password is None else password
        self._port = PORT if port is None else port
        self._charset = CHARSET if charset is None else charset
        self.conn = None
        self.get_conn_result = self.is_connection_db(get_data_method='tuple')
        if self.get_conn_result:  # 只有数据库连接上才获取数据游标
            self._cursor = self.conn.cursor()

    def is_connection_db(self, get_data_method='dict'):
        """
        数据库连接方法，默认获取的数据类型为字典，它以字段为key，以字段下的数据为value
        :param get_data_method:
        :return:
        """
        try:
            if get_data_method == 'dict':
                # 1.获取一行数据，返回的是dict类型，它以数据表中的字段为key，以字段下的数据为value
                # 2.获取多行数据，返回的是tuple类型，tuple序列内容为dict类型，它以数据表中的字段为key，以字段下的数据为value
                self.conn = MySQLdb.connect(host=self._dbhost,
                                            user=self._user,
                                            passwd=self._password,
                                            db=self._dbname,
                                            port=self._port,
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset=self._charset,
                                            )
            elif get_data_method == 'tuple':
                self.conn = MySQLdb.connect(host=self._dbhost,
                                            user=self._user,
                                            passwd=self._password,
                                            db=self._dbname,
                                            port=self._port,
                                            charset=self._charset,
                                            )
            else:
                self._logger.warn("please give correct method for getting data!")
                return False
        except Exception, e:
            self._logger.warn("query database exception,%s" % e)
            return False
        else:
            return True

    def get_more_row(self, sql):
        """
        从数据库中获取多行数据方法
        :param sql:
        :return:
        """
        record = ""
        if self.get_conn_result:
            try:
                self._cursor.execute(sql)
                record = self._cursor.fetchall()  # 获取多行数据函数
                if record == () or record is None:
                    record = False
                self._cursor.close()  # 关闭游标
                self.conn.close()  # 关闭数据库
            except Exception, e:
                record = False
                self._logger.warn("query database exception,sql= %s,%s" % (sql, e))
        return record

    def get_one_row(self, sql):
        """
        从数据库中获取一行数据方法
        :param sql:
        :return:
        """
        record = ""
        if self.get_conn_result:
            try:
                self._cursor.execute(sql)
                record = self._cursor.fetchone()  # 获取多行数据函数
                if record == () or record is None:
                    record = False
                self._cursor.close()  # 关闭游标
                self.conn.close()  # 关闭数据库
            except Exception, e:
                record = False
                self._logger.warn("query database exception,sql= %s,%s" % (sql, e))
        return record

    def modify_sql(self, sql):
        """
        更新、插入、删除数据库数据方法
        :param sql:
        :return:
        """
        flag = False
        if self.get_conn_result:
            try:
                self._cursor.execute(sql)
                self.conn.commit()
                self._cursor.close()
                self.conn.close()
                flag = True
            except Exception, e:
                flag = False
                self._logger.warn("query database exception,sql= %s,%s" % (sql, e))
        return flag
