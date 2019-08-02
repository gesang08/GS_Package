#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import wx
import wx.lib.mixins.inspection
import numpy
import time
import ID_DEFINE
import math
from MyLogCtrl import MyTextCtrl
from MyLogCtrl import MyLog
import UI
from CONST_DEFINE import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def main():
    app = MyApp()
    app.MainLoop()


class MyApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):
        """
        重写wx.App下的OnInit()方法，该方法在程序开始运行时，它会被自动调用，程序正常退出时，它返回False，否则返回True
        :return:
        """
        mainframe = UI.MyFrame(parent=None, id=wx.ID_ANY, title="Package System", pos=wx.DefaultPosition,
                               size=(SCREEN_WIDTH, SCREEN_HEIGHT), style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE)
        """
        1.parent:Frame类的父类，经常为None
        2.id:默认值为-1，wx.ID_ANY的值也等于-1
        3.title:标题栏的Caption名称属性
        4.pos:Frame窗体相对于电脑屏幕左上角的坐标位置，wx.DefaultPosition的值也等于None
        5.size：Frame窗体的宽度和高度大小，wx.DefaultSize的值也等于None
        6.style:
        wx.DEFAULT_FRAME_STYLE包括：wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | 
                                    wx.CLOSE_BOX | wx.CLIP_CHILDREN
        （1）wx.MINIMIZE_BOX：最小化按钮，如果没有它，最小化按钮不使能；
        （2）wx.MAXIMIZE_BOX：最大化按钮，如果没有它，最大化按钮不使能；
        （3）wx.RESIZE_BORDER：可在边框处用鼠标调整Frame窗口大小，如果没有它，Frame窗口不能调整大小
        （4）wx.CAPTION：显示Frame窗口的title,最小化按钮,最大化按钮,关闭按钮最上面的标题栏，如果没有它标题栏不显示
        （5）wx.CLOSE_BOX：关闭按钮，如果没有它，关闭按钮不使能
        （6）wx.SYSTEM_MENU：当style仅有它时，只显示一个Frame窗口，没有标题栏，窗口也不可调
        （7）wx.MAXIMIZE:显示窗口最大化，此时不受size和pos属性限制
        （8）wx.MINIMIZE:显示窗口最小化，此时不受size属性限制
        """
        mainframe.Center(dir=wx.BOTH)
        """
        调用父类wx.Frame下的Center(self, dir=wx.BOTH)
        dir:有3个参数，即wx.HORIZONTAL, wx.VERTICAL，wx.BOTH
        """
        mainframe.Show()
        self.SetTopWindow(mainframe)  # 设置mainframe为顶级窗口
        return True


if __name__ == '__main__':
    main()
