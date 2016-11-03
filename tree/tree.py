#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xiaoyipeng'

#下面_Getch代码来源：
#http://code.activestate.com/recipes/134892/
class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError, err:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        sys.stdout.write('按\'enter\'翻下一页，按‘q’退出')
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdout.write('\b'*29)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

import os, sys

#版本号
version = '1.0.0'
#是否显示所有文件或文件夹，默认不显示
showAll = False
#是否反序输出结果, 默认正序
reverse = False
#目录显示的最多层级，默认显示所有
maxLevel = 0
#翻页显示模式下每页显示的行数，默认不开启翻页模式
size = 0
#排序方式，默认是按名字排序
sortMethod = None
#现在已经输出了多少行，在分页显示时使用
currentPrint = 0
#统计文件夹个数
sumDirectorys = 0
#统计文件个数
sumfiles = 0
#每个文件夹最后多输一个空行（为了好看）
#但是有可能多个空行连着，以这个做为标记已经输出过了(连着的空行不重复输出)
hasBlankLine = False

def printHelp(*args):
    '''打印帮助'''
    if len(args)>0:
        print 'help不能带参数！'
    else:
        print '''这个程序可以打印目录的树形结构, 如果不指定目录则打印当前目录

tree --选项/-选项 [参数] --选项/-选项 [参数] [目录]

选项包括:
    -v/--version   : 显示程序的版本号
    -h/--help      : 显示帮助
    -a/--all       : 显示所有文件或文件夹(包括影藏的和临时的)， 默认不显示
    -s/--size      : 开启翻页显示（按'q'退出，按'enter'继续），参数表示每页显示的行数，默认10行
    -l/--level     : 参数表示最多显示的目录层级，默认显示到最后一级
    -r/--reverse   : 按当前排序方式反序输出结果，默认正序，默认的排序方式是文件名排序
    -at/--atime    : 按最后访问时间排序
    -ct/--ctime    : 按创建时间排序
    -mt/--mtime    : 按最后修改时间排序
    -fs/--filesize : 按文件大小排序'''
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

def setReverse(*args):
    '''设置是否反序输出结果'''
    if len(args)>0:
        print 'reverse不能带参数!'
        exit()
    else:
        global reverse
        reverse = True

def setSize(*args):
    '''设置一行显示几页'''
    global size
    if len(args)==1 and args[0].isdigit():
        size = int(args[0])
    elif len(args)==0:
        #如果size不带参数，默认10
        size = 10
    else:
        print 'size参数不正确!'
        exit()

def setLevel(*args):
    '''设置最多显示的层级'''
    if len(args)==1 and args[0].isdigit():
        global maxLevel
        maxLevel = int(args[0])
    else:
        print 'level参数不正确!'
        exit()

def setATime(*args):
    '''设置按最后访问时间排序'''
    global sortMethod
    if len(args)>0:
        print 'atime不能带参数!'
        exit()
    elif sortMethod is not None:
        print '只能按一种方式排序'
        exit()
    else:
        sortMethod = os.path.getatime

def setCTime(*args):
    '''设置按最后访问时间排序'''
    global sortMethod
    if len(args)>0:
        print 'ctime不能带参数!'
        exit()
    elif sortMethod is not None:
        print '只能按一种方式排序'
        exit()
    else:
        sortMethod = os.path.getctime

def setMTime(*args):
    '''设置按最后访问时间排序'''
    global sortMethod
    if len(args)>0:
        print 'mtime不能带参数!'
        exit()
    elif sortMethod is not None:
        print '只能按一种方式排序'
        exit()
    else:
        sortMethod = os.path.getmtime

def setFileSize(*args):
    '''设置按文件大小排序'''
    global sortMethod
    if len(args)>0:
        print 'filesize不能带参数!'
        exit()
    elif sortMethod is not None:
        print '只能按一种方式排序'
        exit()
    else:
        sortMethod = os.path.getsize

#option对应调的方法名
options = {
    '--version'  : printVersion,
    '-v'         : printVersion,
    '--help'     : printHelp,
    '-h'         : printHelp,
    '--all'      : setShowAll,
    '-a'         : setShowAll,
    '--size'     : setSize,
    '-s'         : setSize,
    '--level'    : setLevel,
    '-l'         : setLevel,
    '--reverse'  : setReverse,
    '-r'         : setReverse,
    '--atime'    : setATime,
    '-at'        : setATime,
    '--ctime'    : setCTime,
    '-ct'        : setCTime,
    '--mtime'    : setMTime,
    '-mt'        : setMTime,
    '--filesize' : setFileSize,
    '-fs'        : setFileSize,
}

def conformOptions(option, *args):
    '''执行option对应的方法'''
    if options.has_key(option):
        options[option](*args)
    else:
        print '不存在' + option + '这个选项！'
        exit()

def checkPath(path):
    '''检查路径是否存在, 如果不存在提示错误，并退出'''
    if os.path.isdir(path):
        return
    else:
        print path + '不是一个目录！'
        exit()

def waitInput():
    '''等待用户输入q退出，或回车继续'''
    while True:
        answer = getch()
        if answer == 'q' or answer == 'Q':
            print '\b'*28+' '*28+'\n', sumDirectorys, '个文件夹, ', sumfiles, '个文件。\n'
            exit()
        elif answer == '\r':
            break

def sortFileName(path, fileNames):
    #如果没有设置排序方式就按文件名排序
    if sortMethod is None:
        return fileNames
    #比较用的方法
    def compareMethod(x, y):
        if sortMethod(os.path.join(path, x)) < sortMethod(os.path.join(path, y)):
            return -1
        else:
            return 1

    return sorted(fileNames, compareMethod)

def treePath(path, levelstr='', level=0):
    '''递归打印文件或文件夹'''
    #如果限制了最多输出的层级并且已经达到了限制，则返回
    if maxLevel!=0 and level>=maxLevel:
        return
    fileNames = os.listdir(path)
    #排序方式
    fileNames = sortFileName(path, fileNames)
    #是否反序
    if reverse:
        fileNames.sort(reverse = True)
    last = len(fileNames)-1
    for (index, name) in enumerate(fileNames):
        #根据showAll忽略.和$开头的文件或文件夹
        if not showAll and (name.startswith('.') or name.startswith('$') or name.startswith('~')):
            continue

        #得到路径
        abspath = os.path.join(path, name)

        #打印文件名，前面加上层级关系的字符串
        printstring = levelstr + '|--' + name
        #因为是用退格的方式清掉翻下一页的提示，所以要用多一些空格覆盖原来的地方
        print printstring + ' '*(28 - len(printstring))
        global hasBlankLine
        hasBlankLine = False
        global currentPrint
        currentPrint+=1
        #开启了翻页
        if size!=0 and currentPrint%size==0:
            #等待用户输入enter
            waitInput()

        if os.path.isdir(abspath):
            global sumDirectorys
            sumDirectorys += 1
            if index == last:
                treePath(abspath, levelstr+'   ', level+1)
            else:
                treePath(abspath, levelstr+'|  ', level+1)
        else:
            global sumfiles
            sumfiles += 1

        if index == last and not hasBlankLine:
            print levelstr + ' '*(28-len(levelstr))
            hasBlankLine = True

def getUserInput():
    '''得到用户的输入'''
    #path是要打印的目录，rang是用户输入选项参数所在的范围
    if len(sys.argv)==1:
        path = os.getcwd()
        rang = []
    #如果指定了目录，必须在最后一个，最后一个也有可能是参数(参数是-开头或者是数字)
    elif not ( sys.argv[len(sys.argv)-1].startswith('-') or sys.argv[len(sys.argv)-1].isdigit() ):
        path = sys.argv[len(sys.argv)-1]
        rang = range(1, len(sys.argv)-1)
    else:
        path = os.getcwd()
        rang = range(1, len(sys.argv))
    args = []
    #处理用户输入的参数, args是最后得到用户输入选项和参数的数组
    for x in rang:
        option = sys.argv[x]
        #这是个数，直接跳过
        if option.isdigit():
            continue
        else:
            arg = [option]
            i = x+1
            while i <= rang[len(rang)-1] and sys.argv[i].isdigit():
                arg.append(sys.argv[i])
                i+=1
            args.append(arg)
    return args, path

if __name__ == '__main__':
    #args是用户输入的选项和参数，path是目录
    args, path = getUserInput()
    for arg in args:
        conformOptions(*arg)
    print path
    # 检查路径是否存在, 如果不存在提示错误，并退出
    checkPath(path)
    # 开始打印
    treePath(path)
    # 打印统计文件和文件夹个数
    print sumDirectorys, '个文件夹, ', sumfiles, '个文件。\n'