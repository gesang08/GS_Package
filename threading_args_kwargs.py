#!/usr/bin/env python
# _*_ coding: UTF-8 _*_


"""
1.使用线程实现每隔1秒钟打印内容ok（实现简单线程功能）
2.*args,**kwargs的理解
"""
import threading
import time


def run():
    while True:
        print 'ok'
        time.sleep(1)


def add(x, y):
    sum = x + y
    return sum


# 当不知道需要向函数或方法中传入的实参个数时，我们可以使用*args, **kwargs形式参数，这样可以处理不定数量的实参
# *args, **kwargs在传实参的时候可以省略不传
def foo_args_kwargs(arg, *args, **kwargs):
    if arg:
        print "string: ", arg
    if args:  # *args是用来把参数打包成元组(tuple)然后给函数体或方法使用
        print "arg: ", args

    if kwargs:  # 打包关键字参数成字典(dict)然后给函数体调用
        print "kwarg: ", kwargs
    res = 0
    if isinstance(args, tuple):     # 通过isinstance(o, t)判断一个实例的类型是否正确
        for e in args:
            res += e
    if isinstance(kwargs, dict):
        for k, v in kwargs.items():
            print k, v
    return res


if __name__ == '__main__':
    print add(1, 3)  # 如果此处传入3个参数，程序就会报错
    print foo_args_kwargs('www', 1, 4, 6, 9, key1=9, key2=0, key3=100)  # 传实参时，必须是（arg , *args , **kwargs）这个顺序，否则程序会报错
    a = [1, 2, 3, 4, 5, 6]
    b = {'www': 1, 'baidu': 2, '.com': 3}
    print foo_args_kwargs('hahaha', *a, **b)  # foo_args_kwargs('hahaha', a, b)：a前面不加一个*，b前面不加两个**，程序会报错

    print "省略向形参**kwargs结果："
    print foo_args_kwargs('hahaha', *a)

    print "省略向形参*args结果："
    print foo_args_kwargs('hahaha', **b)

    print "省略向形参*args和**kwargs结果："
    print foo_args_kwargs('hahaha')

    t = threading.Thread(target=run)
    t.start()

