#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/14 15:38
# @Author  : KuoYu
# @Site    : pythonic.site
# @File    : urls
# @Software: PyCharm

from django.urls import path

from . import views

app_name = 'blog'  # have to add *app_name*, cuz include need differentiate

urlpatterns = [
    path('', views.index, name='home'),
    path(r'article/<int:pk>', views.show_article, name='article-find'),
    path(r'tags/<int:pk>', views.tag_find, name='tag-find'),
    path(r'test_view',views.ArticleView.as_view()),
]
