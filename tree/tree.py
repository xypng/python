#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xiaoyipeng'

import os, sys

version = '1.0.0'
#是否显示所有文件或文件夹
showAll = False

def printHelp():
    '''打印帮助'''
    print '''这个程序可以打印目录的树形结构
    选项包括:
    --version : 显示程序的版本号
    --help    : 显示帮助
    --all     : 显示所有文件或文件夹(包括影藏的和临时的)， 默认不显示'''
    exit()

def printVersion():
    '''打印版本号'''
    print 'version:', version
    exit()

def setShowAll():
    '''设置显示所有目录'''
    global showAll
    showAll = True

def checkPath(path):
    '''检查路径是否存在, 如果不存在提示错误，并退出'''
    if os.path.exists(path):
        return
    else:
        print '请检查路径是否正确！'
        exit()

#option对应调的方法名
options = {
    'version': printVersion,
    'help'   : printHelp,
    'all'    : setShowAll,
}

def conformOptions(option):
    '''执行option对应的方法'''
    if options.has_key(option):
        options[option]()
    else:
        print '输入参数错误！'
        exit()

def treePath(path, level=0):
    '''递归打印文件或文件夹'''
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
    if len(sys.argv)==1:
        path = os.getcwd()
    elif len(sys.argv)==2:
        if sys.argv[1].startswith('--'):
            option = sys.argv[1][2:]
            conformOptions(option)
            path = os.getcwd()
        else:
            path = sys.argv[1]
    elif len(sys.argv)==3:
        if not sys.argv[1]=='--all':
            print '输入参数错误！'
            exit()
        setShowAll()
        path = sys.argv[2]
    else:
        print '输入太多参数！'
        exit()
    #检查路径是否存在, 如果不存在提示错误，并退出
    checkPath(path)
    #开始打印
    treePath(path)