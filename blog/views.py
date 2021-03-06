from django.shortcuts import render, get_object_or_404
from django.views import generic
from markdown import Markdown

from mysite import settings
from . import models
import markdown

# Create your views here.


# 文章列表Base类,指定渲染页面template_name即可
class ListBaseView(generic.ListView):
    model = models.Articles
    context_object_name = 'articles'
    paginate_by = settings.BASE_PAGE_BY
    paginate_orphans = settings.BASE_ORPHANS


#  Index界面需要展示文章的概略信息
class IndexView(ListBaseView):
    template_name = 'blog/index.html'


# Archive界面需要展示文章的归档信息
class ArchiveView(ListBaseView):
    template_name = 'blog/archive.html'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(IndexView, self).get_context_data()
    #
    #


# 文章详细视图
class DetailView(generic.DetailView):
    model = models.Articles
    template_name = 'blog/detail.html'  # TODO
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super(DetailView, self).get_object(queryset=None)
        obj.update_views()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        obj.body = md.convert(obj.body)
        obj.TOC = md.toc
        return obj
    # TODO : add comment ,overwrite get_content_data method


# 指定模型to_find_model去查找文章
class BaseFindView(generic.ListView):
    model = models.Articles
    to_find_model = models.Category
    template_name = 'blog/listbase.html'
    paginate_by = settings.BASE_PAGE_BY
    paginate_orphans = settings.BASE_ORPHANS

    def get_queryset(self):
        obj = get_object_or_404(self.to_find_model, slug=self.kwargs.get('slug'))
        return obj.articles_set.all()


# 父类为BaseFindView
class CategoryView(BaseFindView):
    to_find_model = models.Category


class TagsView(BaseFindView):
    to_find_model = models.Tags

class DateArchiveView(BaseFindView):
    def get_queryset(self):
        year = self.kwargs.get('y')
        month = self.kwargs.get('m')
        obj = self.model.objects.filter(create_date__year=year,create_date__month=month).order_by('-create_date')
        return obj

class AboutView(generic.ListView):
    model = models.TimeLine
    template_name = 'blog/about.html'
    context_object_name = 'timeline_list'


class MySearchView():
    # TODO:全文搜索
    pass
