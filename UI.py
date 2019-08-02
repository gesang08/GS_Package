#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import wx
import wx.lib.mixins.inspection
import time
import re
import MySQLdb
import numpy as np
import package_algorithm
import MyLogCtrl
from CONST_DEFINE import *
import MyDb


class MyFrame(wx.Frame):  # 继承wx.Frame的类
    def __init__(self, parent, id, title, pos, size, style):
        # 重写父类wx.Frame的构造方法，即重构，__init__()即为类的构造函数或构造方法
        wx.Frame.__init__(self, parent, id, title, pos, size, style)  # 继承父类wx.Frame的构造方法
        # 为何要继承父类的构造方法：因为子类会继承父类中的数据，可能还会使用父类的数据（属性，方法），所以在子类初始化前，一定要先完成父类数据的初始化
        self.create_menu_bar()
        # self.create_box()  # 自动产生装箱尺寸函数
        self.panel = wx.Panel(self, -1)
        # self.panel.SetBackgroundColour(colour='Red')
        self.log = self.create_log_text()  # 虽调用create_log_text()方法，实质是实例化MyTextCtrl类
        self.bind_event()
        self.produce_box_dialog = None
        self.box_length_label = None
        self.box_width_label = None
        self.box_height_label = None
        self.box_length_text = None
        self.box_width_text = None
        self.box_height_text = None
        self.CreateStatusBar()  # 创建状态栏
        self.GetStatusBar().SetStatusText("running...")
        self.package = package_algorithm.Package()
        self.db = None

    def create_log_text(self, ctrl_text=""):
        if ctrl_text.strip():
            """
            string.strip(self, chars=None):
            功能：删除string字符串中开头、结尾处chars序列的字符
            默认：默认删除空白符（包括'\n', '\r',  '\t',  ' ')
            """
            value = ctrl_text
        else:
            value = ""
        return MyLogCtrl.WriteLog(self.panel, -1, value, wx.Point(0, SCREEN_HEIGHT - 200), wx.Size(SCREEN_WIDTH, 200),
                                  wx.NO_BORDER | wx.TE_MULTILINE | wx.TE_READONLY)

    def create_menu_bar(self):
        """
        创建UI的菜单栏
        :return:
        """
        start_menu = wx.Menu()
        menu_bar = wx.MenuBar()
        start_menu.Append(id=ID_LOGIN, item="登入")
        start_menu.Append(id=ID_LOGOUT, item="登出")
        start_menu.AppendSeparator()
        start_menu.Append(id=ID_EXIT, item="退出")
        set_menu = wx.Menu()
        set_menu.Append(id=ID_SET, item="produce")
        menu_bar.Append(start_menu, "文件")
        menu_bar.Append(set_menu, "生成")
        self.SetMenuBar(menu_bar)

    def menu_produce_click_response(self, event):
        """
        点击菜单栏中的produce选项，弹出一个界面，用于产生打包盒子的尺寸，箱子只有长宽高、类型属性
        :param event:
        :return:
        """
        self.produce_box_dialog = wx.Dialog(parent=self.panel, title='产生货箱规格', size=(300, 400),
                                            style=wx.DEFAULT_DIALOG_STYLE)
        """
        style:
        wx.DEFAULT_DIALOG_STYLE: wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU
        """
        produce_box_panel = wx.Panel(parent=self.produce_box_dialog, id=-1)
        self.box_length_label = wx.StaticText(parent=produce_box_panel, label='长  度:', pos=(50, 50))
        self.box_width_label = wx.StaticText(parent=produce_box_panel, label='宽  度:', pos=(50, 100))
        self.box_height_label = wx.StaticText(parent=produce_box_panel, label='高  度:', pos=(50, 150))
        self.box_length_text = wx.TextCtrl(parent=produce_box_panel, pos=(100, 50))
        self.box_width_text = wx.TextCtrl(parent=produce_box_panel, pos=(100, 100))
        self.box_height_text = wx.TextCtrl(parent=produce_box_panel, pos=(100, 150))
        box_ok_button = wx.Button(parent=produce_box_panel, label='确定', pos=(25, 250))
        box_cancel_button = wx.Button(parent=produce_box_panel, label='取消', pos=(190, 250))
        box_ok_button.Bind(wx.EVT_BUTTON, self.box_ok_click_response)
        box_cancel_button.Bind(wx.EVT_BUTTON, self.box_cancel_click_response)
        """
        事件绑定Bind()用法：
        结构：Bind(self, event, handler, source, id, id2)
        参数：
            1.event：指出事件类型，如wx.EVT_BUTTON事件；
            2.handler:事件处理器，一般为一个函数或类下面的一个方法；
            3.source:指出事件与哪一个控件对象进行绑定，有两种方法：（1）Bind(event,handler,控件对象)；（2）控件对象.Bind(event,handler)
            4.id:在事件系统里唯一决定窗口的标识符,有三种：（1）系统自动创建；（2）使用标准ID；（3）创建自己的ID
                （1）系统自动创建：如果设置id参数为-1或wx.ID_ANY或默认，wxPyhton会自动创建id，这些自动创建的id通常是负数，可以通过GetId()方法获得其ID；
                （2）创建自己的ID：用户创建的id通常必须为正
                注意：参数id和id2使用ID号指定了事件的源。一般情况下这没必要，因为事件源的ID号可以从参数source中提取，但是在一些
                情况下使用ID是合理的：
                （1）比如在菜单下有多个Item都是通过点击事件响应，这时需要指定个Item的id，以区分不同的Item来绑定点击事件；
                （2）如果同时使用了参数id和id2，就能够以窗口部件的ID号形式将这两个ID号之间范围的窗口控件绑定到事件，
                     这仅适用于窗口部件的ID号是连续的。比如界面上有菜单的一级菜单Item文件和生成，文件下有二级菜单登入，登出，退出3个Item,
                     生成下有二级菜单produce 1个Item,绑定菜单事件Bind(wx.EVT_MENU, 事件处理器，id=id(登入)，id=id(produce)),则
                     点击登入，登出，退出和produce二级菜单会出现同样的事件响应
        """
        self.produce_box_dialog.ShowModal()

    def bind_event(self):
        self.Bind(wx.EVT_MENU, self.menu_produce_click_response, id=ID_SET)

    def box_ok_click_response(self, event):
        regIntOrFloat = '^\d+$' + '|' + '^\d+\.\d+$'  # 整数或小数
        box_length = self.box_length_text.GetValue()
        box_width = self.box_width_text.GetValue()
        box_height = self.box_height_text.GetValue()
        box_type = 'BT' + box_length  # 盒子型号定义：取box和type首字母在加上盒子的长作为盒子型号
        thick_dict = {}
        if re.search(regIntOrFloat, box_length) and re.search(regIntOrFloat, box_width) and \
                re.search(regIntOrFloat, box_height):
            box_length_numeric = float(box_length)
            box_width_numeric = float(box_width)
            box_height_numeric = float(box_height)
            thick_dict['18'] = round(box_height_numeric / 18)
            thick_dict['20'] = round(box_height_numeric / 20)
            thick_dict['22'] = round(box_height_numeric / 22)
            thick_dict['25'] = round(box_height_numeric / 25)
            sql = "INSERT INTO `equipment_package_box` (`Box_type`, `Box_long`, `Box_short`, `Box_height`, " \
                  "`Plies_18mm`, `Plies_20mm`, `Plies_22mm`, `Plies_25mm`) VALUES " \
                  "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                  (box_type, box_length_numeric, box_width_numeric, box_height_numeric,
                   thick_dict['18'], thick_dict['20'], thick_dict['22'], thick_dict['25'])
            try:
                my = MyDb.Database()
                my.modify_sql(sql)
            except:
                self.log.write_textctrl_txt("box_ok_click_response()方法下调用modify_sql()方法出错！ \r")
            else:
                self.log.write_textctrl_txt("成功产生长%smm,宽%smm,高%smm的的纸箱！ \r" %
                                            (box_length_numeric, box_width_numeric, box_height_numeric))
        event.Skip()  # event.skip()的作用是告诉MainLoop继续处理这个消息，而不是在当前handler处理完了就中断了，
        # 就是说如果其他的parent的窗口或者paragate窗口还有相应的handler时，也应该调用他们。

    def box_cancel_click_response(self, event):
        self.produce_box_dialog.Close()

    def create_box(self):
        """
        产生纸盒尺寸，定义最小的为650*450；长度<2436，宽度<1200
        纸盒尺寸生产分三阶段：
        1.长度650-1200，以150为等差数列
        2.长度1200-1800，以200为等差数列
        3.1800-2436，以250为等差数列
        宽度方向均以150为等差数列,箱子的类型以BT+length来定义
        :return:总计11*6=66个类型纸箱
        """
        length = [650, 800, 950, 1100, 1200, 1400, 1600, 1800, 2050, 2300, 2436]
        width = [450, 600, 750, 900, 1050, 1200]
        for i in range(len(length)):
            for j in range(len(width)):
                h = int(round(60 * (10 ** 9) / (length[i] * width[j] * BaseMaterialDensity)))
                my = MyDb.Database()
                sql = "INSERT INTO `equipment_package_box` (`Box_type`, `Box_long`, `Box_short`, `Box_height`, `State`) VALUES ('%s', '%s', '%s', '%s', '%s')" % ('BT' + str(length[i]), length[i], width[j], h, 5)
                my.modify_sql(sql)
        print length
