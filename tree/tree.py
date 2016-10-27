#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xiaoyipeng'

import os, sys

#版本号
version = '1.0.0'
#是否显示所有文件或文件夹，默认不显示
showAll = False
#目录显示的最多层级，默认显示所有
maxLevel = 0
#翻页显示模式下每页显示的行数，默认不开启翻页模式
size = 0

def printHelp(*args):
    '''打印帮助'''
    if len(args)>0:
        print 'help不能带参数！'
    else:
        print '''这个程序可以打印目录的树形结构, 如果不指定目录则打印当前目录
    选项包括:
        -v/--version : 显示程序的版本号
        -h/--help    : 显示帮助
        -a/--all     : 显示所有文件或文件夹(包括影藏的和临时的)， 默认不显示
        -s/--size    : 开启翻页显示，参数表示每页显示的行数，默认10行
        -l/--level   : 参数表示最多显示的目录层级，默认显示到最后一级'''
    exit()

def printVersion(*args):
    '''打印版本号'''
    if len(args)>0:
        print 'version不能带参数！'
    else:
        print 'version:', version
    exit()

def setShowAll(*args):
    '''设置显示所有目录'''
    if len(args)>0:
        print 'all不能带参数!'
        exit()
    else:
        global showAll
        showAll = True

def setSize(*args):
    '''设置一行显示几页'''
    global size
    if len(args)==1 and args[0].isdigit():
        size = int(args[0])
        print 'size:', size, isinstance(size, int)
    elif len(args)==0:
        #如果size不带参数，默认10
        size = 10
        print 'size:', size, isinstance(size, int)
    else:
        print 'size参数不正确!'
        exit()

def setLevel(*args):
    '''设置最多显示的层级'''
    if len(args)==1 and args[0].isdigit():
        global maxLevel
        maxLevel = int(args[0])
        print 'level:', maxLevel, isinstance(maxLevel, int)
    else:
        print 'level参数不正确!'
        exit()

#option对应调的方法名
options = {
    '--version': printVersion,
    '-v'       : printVersion,
    '--help'   : printHelp,
    '-h'       : printHelp,
    '--all'    : setShowAll,
    '-a'       : setShowAll,
    '--size'   : setSize,
    '-s'       : setSize,
    '--level'  : setLevel,
    '-l'       : setLevel,
}

def conformOptions(option, *args):
    '''执行option对应的方法'''
    if options.has_key(option):
        options[option](*args)
    else:
        print '输入参数错误！'
        exit()

def checkPath(path):
    '''检查路径是否存在, 如果不存在提示错误，并退出'''
    if os.path.exists(path):
        return
    else:
        print '请检查路径是否正确！'
        exit()

def treePath(path, level=0):
    '''递归打印文件或文件夹'''
    #如果限制了最多输出的层级并且已经达到了限制，则返回
    if maxLevel!=0 and level>=maxLevel:
        return
    fileNames = os.listdir(path)
    for name in fileNames:
        #根据showAll忽略.和$开头的文件或文件夹
        if not showAll and (name.startswith('.') or name.startswith('$') or name.startswith('~')):
            continue

        #得到路径
        abspath = os.path.join(path, name)

        #打印文件名，前面加上层级关系的字符串
        print '|  ' * level + '|--' + name

        if os.path.isdir(abspath):
            treePath(abspath, level+1)

if __name__ == '__main__':
    #path是要打印的目录，range是用户输入参数所在的范围
    if len(sys.argv)==1:
        path = os.getcwd()
        range = []
    #如果指定了目录，必须在最后一个，最后一个也有可能是参数(参数是-开头或者是数字)
    elif not ( sys.argv[len(sys.argv)-1].startswith('-') or sys.argv[len(sys.argv)-1].isdigit() ):
        path = sys.argv[len(sys.argv)-1]
        range = range(1, len(sys.argv)-1)
    else:
        path = os.getcwd()
        range = range(1, len(sys.argv))
    args = []
    #处理用户输入的参数, args是最后得到用户输入选项和参数的数组
    for x in range:
        option = sys.argv[x]
        #这是个数，直接跳过
        if option.isdigit():
            continue
        else:
            arg = [option]
            i = x+1
            while i <= range[len(range)-1] and sys.argv[i].isdigit():
                arg.append(sys.argv[i])
                i+=1
            args.append(arg)

    for arg in args:
        print arg
        conformOptions(*arg)

    # 检查路径是否存在, 如果不存在提示错误，并退出
    checkPath(path)
    # 开始打印
    treePath(path)