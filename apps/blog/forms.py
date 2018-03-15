#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/14 15:16
# @Author  : KuoYu
# @Site    : pythonic.site
# @File    : forms
# @Software: PyCharm

from django.forms import ModelForm

from . import models


class ArticlesForm(ModelForm):
    class Meta:
        model = models.Articles
        exclude = ('author',)


class CommentsForm(ModelForm):
    class Meta:
        model = models.Comments


class TagsForm(ModelForm):
    class Meta:
        model = models.Tags
