from django.db import models

from mysite.settings import DEFAULT_AUTHOR


# Create your models here.

class Articles(models.Model):
    title = models.CharField(u'标题', max_length=20)
    create_date = models.DateTimeField(u'创建时间', auto_now_add=True)
    revise_date = models.DateTimeField(u'修改时间', auto_now=True)
    revise_freq = models.IntegerField(u'修改次数', default=0)
    content = models.TextField(u'内容')
    author = models.CharField(u'作者', max_length=10, default=DEFAULT_AUTHOR)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-create_date',)


class Comments(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=20, default="Guest")
    comment = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)


class Tags(models.Model):
    tag_name = models.CharField(max_length=5)
    article_inner = models.ManyToManyField(Articles)

    def __str__(self):
        return self.tag_name
