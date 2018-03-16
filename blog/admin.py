from django.contrib import admin

# Register your models here.
from . import models


# 自定义管理站点的名称和URL标题
admin.site.site_header = '网站管理'
admin.site.site_title = '博客后台管理'


@admin.register(models.Articles)
class ArticlesAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_date'
    exclude = ('views',)

    list_display = ('title', 'author', 'create_date', 'update_date')
    list_per_page = 50
    filter_horizontal = ('tags', 'keywords')

    def get_queryset(self, request):
        qs = super(ArticlesAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)



@admin.register(models.Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug')

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug')



@admin.register(models.TimeLine)
class TimelineAdmin(admin.ModelAdmin):
    list_display = ('title', 'side', 'update_date', 'icon', 'icon_color',)
    fieldsets = (
        ('图标信息', {'fields': (('icon', 'icon_color'),)}),
        ('时间位置', {'fields': (('side', 'update_date', 'star_num'),)}),
        ('主要内容', {'fields': ('title', 'content')}),
    )
    date_hierarchy = 'update_date'
    list_filter = ('star_num', 'update_date')

@admin.register(models.Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'content', 'img_url', 'url')


@admin.register(models.KeyWords)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

@admin.register(models.FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'link', 'create_date', 'is_active', 'is_show')
    date_hierarchy = 'create_date'
    list_filter = ('is_active', 'is_show')
