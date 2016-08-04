#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = 'xiaoyipeng'

import urllib
import urllib2
import re

htmlCharacterMap = {
	'<br/>' : '\n',
	'&quot;' : '"',
	'&nbsp;' : ' ',
	'&gt;' : '>',
	'&lt;' : '<',
	'&amp;': '&',
	'&#39':"'",
}

class QSBK(object):
	"""糗事百科的爬虫"""
	def __init__(self):
		self.pageIndex = 1
		self.pagetotal = 9999
		self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4)'
		self.headers = {'User-Agent' : self.user_agent}
		self.stories = []
		self.enable = False

	def getPageContent(self, pageIndex):
		try:
			url = 'http://www.qiushibaike.com/8hr/page/%d/' % pageIndex
			request = urllib2.Request(url, headers=self.headers)
			response = urllib2.urlopen(request)
			pageContent = response.read().decode('utf-8')
			return pageContent
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print u"连接糗事百科失败，错误原因：", e.reason
				return None

	def getPageTotal(self, content):
		"""得到总页数"""
		if self.pagetotal != 9999:
			print 'page=%d' % self.pageIndex
			return
		pattrenStr = '<span class="page-numbers">(?P<pagetotal>.*?)</span>'
		pattern = re.compile(pattrenStr, re.S)
		items = re.findall(pattern, content)
		if len(items)>0:
			self.pagetotal = int(items[-1].strip())
			print 'totalpage=%d' % self.pagetotal

	def getPageItems(self, pageIndex):
		pageContent = self.getPageContent(pageIndex)
		if not pageContent:
			print "页面加载失败..."
			return None
		self.getPageTotal(pageContent)
		pattrenStr = r'<div class="article block untagged mb15".*?">.*?'\
						r'.*?<h2>(?P<authorname>.*?)</h2>.*?'\
						r'<div class="content">(?P<content>.*?)</div>'\
						r'(?P<maybehaveimage>.*?)'\
						r'<i class="number">(?P<numbervote>.*?)</i>.*?'\
						r'</div>'
		pattern = re.compile(pattrenStr, re.S)
		items = re.findall(pattern, pageContent)
		return items

	def getNextPage(self):
		if self.pageIndex > self.pagetotal:
			self.enable = False
			print "你已经看完所有的"
			return
		items = self.getPageItems(self.pageIndex)
		self.pageIndex += 1
		for item in items:
			#如果有图片直接跳过，因为图片在终端显示不了
			if re.search('img', item[2]):
				continue
			content = item[1].strip()
			#转换html的特殊字符
			for (k,v) in htmlCharacterMap.items():
				content = re.sub(re.compile(k), v, content)
			authorname = item[0].strip() 
			for (k,v) in htmlCharacterMap.items():
				authorname = re.sub(re.compile(k), v, authorname)
			self.stories.append(authorname + 
			'(' + item[3].strip() + ')' + 
			'\n' + content + '\n')

	def getOneStory(self):
		#防止有的页面全是带图片的
		while (len(self.stories)==0 and self.enable):
			self.getNextPage()
		story = self.stories[0]
		print story
		self.stories.pop(0)
		if len(self.stories)==0:
			self.getNextPage()

	def start(self):
		print u"正在读取糗事百科，按回车查看新段子，Q退出"
		self.enable = True
		self.getNextPage()
		while self.enable:
			input = raw_input()
			if input.upper() == "Q":
				self.enable = False
			else:
				self.getOneStory()

if __name__ == '__main__':
	spider = QSBK()
	spider.start()


