import emoji
import markdown
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField(u'文章分类', max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField('描述', max_length=160,
                                   blank=True, help_text=u'用于描述分类作用')
    keymap = ('name', 'slug', 'description')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_abs_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

    def get_article_list(self):
        return Articles.objects.filter(category=self)


class Tags(models.Model):
    name = models.CharField(u'文章标签', max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField(u'描述', max_length=160,
                                   blank=True, help_text=u'用于描述标签作用')
    keymap = ('name', 'slug', 'description')

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_abs_url(self):
        return reverse('blog:tags', kwargs={'slug': self.slug})

    def get_article_list(self):
        return self.articles_set.all()


class KeyWords(models.Model):
    name = models.CharField(u'文章关键词', max_length=20, help_text=u'用于概括文章主要内容，用逗号分隔')
    keymap = ('name',)

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Articles(models.Model):
    IMG_LINK = settings.DEFAULT_IMG_URL
    # author = models.ForeignKey(settings.DEFAULT_AUTHOR,
    #                            verbose_name=u'作者', max_length=10, on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(u'标题', max_length=150)
    summary = models.CharField(u'摘要', max_length=160)
    body = models.TextField(u'内容')
    img_link = models.CharField(u'主题图片地址', default=IMG_LINK, max_length=260)

    create_date = models.DateTimeField(u'创建时间', default=timezone.now)
    update_date = models.DateTimeField(u'修改时间', auto_now=True)
    revise_freq = models.IntegerField(u'修改次数', default=0)
    views = models.IntegerField(u'阅读量', default=0)
    slug = models.SlugField(u'Slug', unique=True)

    category = models.ForeignKey(Category, verbose_name=u'分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, verbose_name=u'标签')
    keywords = models.ManyToManyField(KeyWords, verbose_name=u'关键词', help_text='文章关键词')


    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.title[:20]

    def get_abs_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views', ])

    def inc_update_freq(self):
        self.update_date = timezone.now()
        self.revise_freq += 1
        self.save(update_fields=['update_date', 'revise_freq'])

    def get_pre(self):
        return Articles.objects.filter(id__lt=self.id).order_by('id').last()

    def get_next(self):
        return Articles.objects.filter(id__gt=self.id).order_by('id').first()

    # 多对多关系获取QuerySet
    def get_tags(self):
        return self.tags.all()

    def get_keywords(self):
        return self.keywords.all()

    # foreign key 直接指定
    def get_category(self):
        return self.category

    def get_author(self):
        return "KuoYu"


# 开发时间线
class TimeLine(models.Model):
    COLOR_CHOICE = (
        ('primary', '基本-蓝色'),
        ('success', '成功-绿色'),
        ('info', '信息-天蓝色'),
        ('warning', '警告-橙色'),
        ('danger', '危险-红色')
    )
    SIDE_CHOICE = (
        ('L', '左边'),
        ('R', '右边'),
    )
    STAR_NUM = (
        (1, '1颗星'),
        (2, '2颗星'),
        (3, '3颗星'),
        (4, '4颗星'),
        (5, '5颗星'),
    )
    side = models.CharField('位置', max_length=1, choices=SIDE_CHOICE, default='L')
    star_num = models.IntegerField('星星个数', choices=STAR_NUM, default=3)
    icon = models.CharField('图标', max_length=50, default='fa fa-pencil')
    icon_color = models.CharField('图标颜色', max_length=20, choices=COLOR_CHOICE, default='info')
    title = models.CharField('标题', max_length=100)
    update_date = models.DateTimeField('更新时间', default=timezone.now)
    content = models.TextField('主要内容')

    class Meta:
        verbose_name = '时间线'
        verbose_name_plural = verbose_name
        ordering = ['update_date']

    def __str__(self):
        return self.title[:20]

    def title_to_emoji(self):
        return emoji.emojize(self.title, use_aliases=True)

    def content_to_markdown(self):
        # 先转换成emoji然后转换成markdown
        to_emoji_content = emoji.emojize(self.content, use_aliases=True)
        return markdown.markdown(to_emoji_content,
                                 extensions=['markdown.extensions.extra', ]
                                 )


# 首页幻灯片
class Carousel(models.Model):
    number = models.IntegerField('编号', help_text='编号决定图片播放的顺序，图片不要多于5张')
    title = models.CharField('标题', max_length=20, blank=True, null=True, help_text='标题可以为空')
    content = models.CharField('描述', max_length=80)
    img_url = models.CharField('图片地址', max_length=200)
    url = models.CharField('跳转链接', max_length=200, default='#', help_text='图片跳转的超链接，默认#表示不跳转')

    class Meta:
        verbose_name = '图片轮播'
        verbose_name_plural = verbose_name
        ordering = ['number', 'id']

    def __str__(self):
        return self.content[:25]


# 友联
class FriendLink(models.Model):
    name = models.CharField('网站名称', max_length=50)
    description = models.CharField('网站描述', max_length=100, blank=True)
    link = models.URLField('友链地址', help_text='请填写http或https开头的完整形式地址')
    logo = models.URLField('网站LOGO', help_text='请填写http或https开头的完整形式地址', blank=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    is_active = models.BooleanField('是否有效', default=True)
    is_show = models.BooleanField('是否首页展示', default=False)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['create_date']

    def __str__(self):
        return self.name

    def get_home_url(self):
        '''提取友链的主页'''
        u = re.findall(r'(http|https://.*?)/.*?', self.link)
        home_url = u[0] if u else self.link
        return home_url

    def active_to_false(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def show_to_false(self):
        self.is_show = True
        self.save(update_fields=['is_show'])
