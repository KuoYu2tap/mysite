from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class MyUser(AbstractUser):
    link = models.URLField(verbose_name=u'个人站点', blank=True, help_text=u'以http(s)开头的站点')
    avatar = None

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id', ]

    def __str__(self):
        return self.username
