#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xiaoyipeng'

import os

def treePath(path, level):
    fileNames = os.listdir(path)
    for name in fileNames:
        #忽略.和$开头的文件或文件夹
        if name.startswith('.') or name.startswith('$'):
            continue

        #得到路径
        abspath = os.path.join(path, name)

        #打印文件名，前面加上层级关系的字符串
        print ''.join(['|  ']*level) + '|--' + name

        if os.path.isdir(abspath):
            treePath(abspath, level+1)

if __name__ == '__main__':
    treePath(os.getcwd(), 0)