from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from django.views import generic

from . import models

# Create your views here.
locals_tags = models.Tags.objects.all()


# 主页展示文章，且利用paginator进行分页
def index(request):
    articles_list = models.Articles.objects.all()
    paginator = Paginator(articles_list, 10)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return render(request, 'blog/list_article.html', {'articles': articles, 'locals_tags': locals_tags})


# 展示单页文章
def show_article(request, pk):
    article = get_object_or_404(models.Articles, id=pk)
    # article.content = markdown(article.content,
    #                            extensions=[
    #                                'markdown.extensions.extra',
    #                                'markdown.extensions.codehilite',
    #                                'markdown.extensions.toc',
    #                            ])
    tags = article.tags_set.all()
    comments = models.Comments.objects.filter(article_id=article)
    # 查找与文章相同tags但非本文的文章进行推荐
    similar = models.Articles.objects.filter(tags__in=tags).filter(~Q(id=pk))
    c = {'article': article, 'tags': tags, 'comments': comments, 'similar': similar, 'locals_tags': locals_tags}
    return render(request, 'blog/show_article.html', c)


# 查找主键为pk的tag的所有文章
def tag_find(request, pk):
    tag = models.Tags.objects.filter(id=pk)
    if tag is None:
        return Http404
    articles = tag[0].article_inner.all()
    return render(request, 'blog/list_article.html', {'articles': articles, 'locals_tags': locals_tags})
