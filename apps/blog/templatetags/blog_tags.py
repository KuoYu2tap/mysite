#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/14 22:25
# @Author  : KuoYu
# @Site    : pythonic.site
# @File    : tags
# @Software: PyCharm

import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from blog import models as blogModels

register = template.Library()  # 自定义filter时必须加上


@register.filter(is_safe=True)  # 注册template filter
@stringfilter  # 希望字符串作为参数
def to_markdown(value):
    return mark_safe(markdown.markdown(
        value,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ],
        safe_mode=True,
        enable_attributes=False))


