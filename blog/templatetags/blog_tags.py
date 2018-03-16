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

from .. import models

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


# TODO: 使用tag直接生成文本？
@register.inclusion_tag('tagsfiles/article_single.html')
def show_articles():
    articles = models.Articles.objects.all()
    return {'object_list': articles}


# TODO 生成nav界面，展示（个人信息，日期归档，标签归档，标签云）
@register.inclusion_tag('tagsfiles/right_nav.html')
def show_right_nav():
    # TODO: about
    about = None
    date_category = models.Articles.objects.all()
    category = models.Category.objects.all()
    tags = models.Tags.objects.all()
    content = {
        'about': about,
        'date_category': date_category,
        'category': category,
        'tags': tags,
    }
    return content


@register.simple_tag
def find_article_tags(article):
    tags = article.tags_set.all()
    return {'artice_tags': tags}

@register.simple_tag
def circle_articles(cur_page, loop_page):
    offset = abs(cur_page - loop_page)
    if offset < 5:
        if cur_page == loop_page:
            page_ele = '<li class="{}"><a href="?page={}">{}</a></li>'.format(loop_page, loop_page)
        else:
            page_ele = '<li><a href="?page={}">{}</a></li>'.format(loop_page,loop_page)
        return page_ele
    else:
        return ''