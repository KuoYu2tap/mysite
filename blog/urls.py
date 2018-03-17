#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/14 15:38
# @Author  : KuoYu
# @Site    : pythonic.site
# @File    : urls
# @Software: PyCharm

from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'blog'  # have to add *app_name*, cuz include need differentiate

urlpatterns = [
    path(r'',RedirectView.as_view(url='index/')),
    path(r'index/',views.IndexView.as_view(), name='home'),
    path(r'detail/<slug:slug>', views.DetailView.as_view(), name='detail'),
    path(r'tags/<slug:slug>', views.TagsView.as_view(), name='tags'),
    path(r'category/<slug:slug>', views.CategoryView.as_view(), name='category'),
    path(r'archive/',views.ArchiveView.as_view(),name='archive-page'),
    path(r'archive/<int:y>/<int:m>', views.DateArchiveView.as_view(), name='date-archive'),
    path(r'about/',views.AboutView.as_view(),name='about'),
]
