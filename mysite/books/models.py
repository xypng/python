# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

class Publisher(models.Model):
    name = models.CharField(u'名称', max_length=30)
    address = models.CharField(u'地址', max_length=50)
    city = models.CharField(u'城市', max_length=60)
    state_province = models.CharField(u'省', max_length=30)
    country = models.CharField(u'国家', max_length=50)
    website = models.URLField(u'网址')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
            

class Author(models.Model):        
    first_name = models.CharField(u'名', max_length=30)
    last_name = models.CharField(u'姓', max_length=40)
    email = models.EmailField(u'邮箱')
    test = models.CharField(u'测试', max_length=30, default=None, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Book(models.Model):
    title = models.CharField(u'标题', max_length=100)
    authors = models.ManyToManyField(Author, verbose_name = u'作者')
    Publisher = models.ForeignKey(Publisher, verbose_name = u'出版社')
    publication_date = models.DateField(u'出版日期')

    def __str__(self):
        return self.title