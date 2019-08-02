#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import wx
import time
import datetime
import MySQLdb
from CONST_DEFINE import *
import MyDb
import os


class MyLog(wx.Log):
    def __init__(self, textCtrl, logTime=0):
        wx.Log.__init__(self)
        self.tc = textCtrl
        self.logTime = logTime

    def DoLogText(self, message):
        if self.tc:
            self.tc.AppendText(message + '\n')


class MyTextCtrl(wx.TextCtrl):
    def __init__(self, parent, id=-1, title="", position=wx.Point(0, 0), size=wx.Size(150, 90),
                 style=wx.NO_BORDER | wx.TE_MULTILINE | wx.TE_READONLY):
        self.parent = parent
        wx.TextCtrl.__init__(self, parent, id, title, position, size, style)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDown)
        # self.My_timer = wx.PyTimer(self.My_Notify)  # 添加时间事件，制定时间事件处理函数为My_Notify（）
        # self.My_timer.Start(1000)  # 设定计时间隔为1秒
        # self.t = time.localtime(time.time())
        # self.filename = time.strftime("%Y%m%d%H.log", self.t)
        # repeat=0

    def OnLeftDown(self, evt):
        pass

    def SaveLogFile(self):
        t = time.localtime(time.time())
        filename = time.strftime("%Y%m%d%H.log", t)
        file = open(filename, 'w+')
        content = self.GetValue().encode('UTF-8')
        file.write(content)
        file.close()
        self.SetValue("")

    def WriteText(self, text, enable=True, font=wx.NORMAL_FONT, colour=wx.BLACK):
        if enable:
            t = time.localtime(time.time())
            st = time.strftime("%Y年%m月%d日 %H:%M:%S  ", t)
            db = MySQLdb.connect(host=SERVER_IP, user=USER, passwd=PASSWORD, db=DB, charset=CHARSET)
            cursor = db.cursor()
            sql = "INSERT INTO `info_log`(`error_occurance_time`,`event`)VALUES('%s','%s')" % \
                  (datetime.datetime.now(), text)
            cursor.execute(sql)
            db.commit()
            text = st + text
            wx.TextCtrl.SetFont(self, font)
            wx.TextCtrl.SetForegroundColour(self, colour)
            # wx.TextCtrl.SetBackgroundColour(self,backgroundcolour)
            try:
                wx.TextCtrl.WriteText(self, text)
            except Exception as e:
                wx.TextCtrl.WriteText(self, st + str(e))


# @author: gs
class WriteLog(wx.TextCtrl):
    """
    三种记录日志的方法：1.记录日志到界面的日志TextCtrl;2.记录日志到数据库info_log表；3.记录日志到项目文件下的log.txt
    """
    def __init__(self, parent, id=-1, value="", pos=wx.Point(0, 0), size=wx.Size(150, 90),
                 style=wx.NO_BORDER | wx.TE_MULTILINE | wx.TE_READONLY):  # value即是TextCtrl中的Text的值
        wx.TextCtrl.__init__(self, parent, id, value, pos, size, style)
        self.log_file = 'log.txt'
        self.log_table_name = 'info_log'

    def write_textctrl_db(self, text, enable=True, font=wx.NORMAL_FONT, colour=wx.BLACK):
        """
        写日志到TextCtrl和数据库中
        :param text:
        :param enable:
        :param font:
        :param colour:
        :return:
        """
        if enable:
            sql = "INSERT INTO `%s`(`error_occurance_time`,`event`) VALUES ('%s','%s')" % \
                  (self.log_table_name, datetime.datetime.now(), text)
            try:
                mydb = MyDb.Database()
                mydb.modify_sql(sql)
            except Exception as e:
                wx.TextCtrl.WriteText(self, current_time() + str(e))
            text = current_time() + text
            wx.TextCtrl.SetFont(self, font)
            wx.TextCtrl.SetForegroundColour(self, colour)
            try:
                wx.TextCtrl.WriteText(self, text)
            except Exception as e:
                wx.TextCtrl.WriteText(self, current_time() + str(e))

    def write_textctrl_txt(self, text, enable=True, font=wx.NORMAL_FONT, colour=wx.BLACK):
        if enable:
            text = current_time() + text
            all_files = os.listdir(os.getcwd())  # 获取当前工程项目文件夹下所有文件名
            if self.log_file not in all_files:  # 若该文件不存在，在当前目录创建一个日志文件
                self.log_file = open(self.log_file, 'w+')
                self.log_file.close()
                self.log_file = self.log_file.name
            with open(self.log_file, 'a+') as file_obj:  # 向日志文件加log
                file_obj.write(text)
            wx.TextCtrl.SetFont(self, font)
            wx.TextCtrl.SetForegroundColour(self, colour)
            try:
                wx.TextCtrl.WriteText(self, text)
            except Exception as e:
                wx.TextCtrl.WriteText(self, current_time() + str(e))


def current_time():
    t = time.localtime(time.time())
    st = time.strftime("%Y年%m月%d日 %H:%M:%S  ", t)
    return st

