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
		self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
		self.headers = {'User-Agent' : self.user_agent}
		self.stories = []
		self.comments = []
		self.currentStoryId = ''
		#是否要退出了
		self.enable = False
		#记录当前是否在查看评论
		self.viewComment = False

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

	def getCommentsContent(self, storyId):
		"""得到段子的评论"""
		try:
			url = 'http://www.qiushibaike.com/article/%s' % storyId
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
			print u'加载第%d页' % self.pageIndex
			return
		pattrenStr = '<span class="page-numbers">(?P<pagetotal>.*?)</span>'
		pattern = re.compile(pattrenStr, re.S)
		items = re.findall(pattern, content)
		if len(items)>0:
			self.pagetotal = int(items[-1].strip())
			print u'总共有%d页' % self.pagetotal

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
						r'<a href="/article/(?P<storyid>.*?)".*?'\
						r'<i class="number">(?P<numbercomment>.*?)</i>.*?'\
						r'</div>'
		pattern = re.compile(pattrenStr, re.S)
		items = re.findall(pattern, pageContent)
		return items

	def getCurrentStoryComments(self, storyId):
		#切换到查看评论模式
		self.viewComment = True
		content = self.getCommentsContent(storyId)
		if not content:
			print "页面加载失败..."
			return None
		reStr = r'<div id="comment-.*?'\
					r'<a href="/users/.*?/" class="userlogin" target="_blank" title="(?P<username>.*?)">(?P=username)</a>.*?'\
					r'<span class="body">(?P<comment>.*?)</span>.*?'\
					r'<div class="report">(?P<index>.*?)</div>'
		pattern = re.compile(reStr, re.S)
		items = re.findall(pattern, content)
		del self.comments[:]
		for item in items:
			comentstr = item[0]+'('+ item[2] + u'楼)' + '\n' + item[1] + '\n'
			for (k,v) in htmlCharacterMap.items():
				re.sub(re.compile(k), v, comentstr)
			self.comments.append(comentstr)
		if len(self.comments)>0:
			print '已切换到查看评论，换回车显示下一个评论,按Q退出回到查看糗事'
		else:
			print '当前糗事没有评论'
			self.viewComment = False

	def getNextPage(self):
		if self.pageIndex > self.pagetotal:
			self.enable = False
			print "你已经看完所有的糗事，现在自动退出！"
			return
		items = self.getPageItems(self.pageIndex)
		self.pageIndex += 1
		for item in items:
			#如果有图片直接跳过，因为图片在终端显示不了
			if re.search('img', item[2]):
				continue
			content = item[1].strip()
			for (k,v) in htmlCharacterMap.items():
			#转换html的特殊字符
				content = re.sub(re.compile(k), v, content)
			authorname = item[0].strip() 
			for (k,v) in htmlCharacterMap.items():
				authorname = re.sub(re.compile(k), v, authorname)
			self.stories.append(authorname + 
			'(' + item[3].strip() + u'好笑·' + str(item[5]) + u'评论)' + 
			'\n' + content + '\n')
			self.stories.append(item[4])

	def getNextComment(self):
		print self.comments[0]
		self.comments.pop(0)
		if len(self.comments)==0:
			print '你已查看完这个糗事的所有评论,现在自动退出到查看糗事'
			self.viewComment = False

	def getOneStory(self):
		#防止有的页面全是带图片的
		while (len(self.stories)==0 and self.enable):
			self.getNextPage()
		story = self.stories[0]
		self.currentStoryId = self.stories[1]
		print story
		self.stories.pop(0)
		self.stories.pop(0)
		if len(self.stories)==0:
			self.getNextPage()

	def start(self):
		print u"正在读取糗事百科，按回车查看下一个糗事，按C查看当前这个糗事的评论，按Q退出或返回"
		self.enable = True
		self.getNextPage()
		while self.enable:
			input = raw_input()
			if input.upper() == "Q":
				if not self.viewComment:
					self.enable = False
				else:
					self.viewComment = False
					print '现在退出到查看糗事了'
			elif input.upper() == "C":
				#查看当前看到的糗事的评论
				if len(self.currentStoryId)>0:
					self.getCurrentStoryComments(self.currentStoryId)
				else:
					print '请先查看糗事再看评论。'
			else:
				if not self.viewComment:
					self.getOneStory()
				else:
					self.getNextComment()

if __name__ == '__main__':
	spider = QSBK()
	spider.start()


