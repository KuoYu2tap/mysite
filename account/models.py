from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


# Create your models here.

class Account(models.Model):
    TAGS_CHOICE = (
        ('foods', '三餐'),
        ('snacks', '零食'),
        ('clothing', '服饰'),
        ('viaticum', '出行'),
        ('learn', '学习'),
        ('life','生活'),
        ('social','社交'),
        ('entertainment', '娱乐'),
        ('healthy', '健康'),
        ('telephone', '电话费'),
        ('medicine', '医疗'),
        ('others', '其他'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(verbose_name='消费原因', choices=TAGS_CHOICE, default='foods', max_length=20)
    cost = models.FloatField(verbose_name='花费')
    describe = models.CharField(verbose_name='描述', max_length=20, blank=True, help_text='输入消费描述(小于20字)')
    spent_date = models.DateField(default=now)

    class Meta:
        verbose_name = '账单'
        verbose_name_plural = verbose_name
        ordering = ['-spent_date']

    def __str__(self):
        return "{}-{}".format(self.get_reason_display(), self.cost)

    def get_cn_reason(self):
        return self.get_reason_display()
