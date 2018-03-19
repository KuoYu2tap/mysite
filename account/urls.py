#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/19 8:52
# @Author  : KuoYu
# @Site    : pythonic.site
# @File    : urls
# @Software: PyCharm

from django.urls import path
from .views import AccountView

app_name = 'account'
urlpatterns = [
    path(r'',AccountView.as_view(),name='detail'),
]