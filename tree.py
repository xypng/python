#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xiaoyipeng'

import os, sys

def treePath(path, level=0):
    fileNames = os.listdir(path)
    for name in fileNames:
        #忽略.和$开头的文件或文件夹
        if name.startswith('.') or name.startswith('$') or name.startswith('~'):
            continue

        #得到路径
        abspath = os.path.join(path, name)

        #打印文件名，前面加上层级关系的字符串
        print '|  ' * level + '|--' + name

        if os.path.isdir(abspath):
            treePath(abspath, level+1)

if __name__ == '__main__':
    #如果没有传入指定目录就打印当前目录，如果传入了就打印指定目录的
    if len(sys.argv)==1:
        treePath(os.getcwd())
    elif len(sys.argv)>1:
        treePath(sys.argv[1])