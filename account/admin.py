from django.contrib import admin

from .models import Account


# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    date_hierarchy = 'spent_date'
    list_filter = ('reason',)
    list_per_page = 20
    list_display = ('reason', 'describe', 'cost')

    def get_queryset(self, request):
        qs = super(AccountAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    #
    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    #     if db_field.name == 'user':
    #         kwargs['queryset'] = User.objects.filter(username=request.user.username)
    #     return super(AccountAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    #
    # def get_readonly_fields(self, request, obj=None):
    #     if obj is not None:
    #         return self.readonly_fields + ('user',)
    #     return self.readonly_fields
    #
    # def add_view(self, request, form_url='', extra_context=None):
    #     data = request.GET.copy()
    #     print(data)
    #     data['user'] = request.user
    #     print("request: ",request)
    #     request.GET = data
    #     return super(AccountAdmin, self).add_view(request, form_url, extra_context=extra_context)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('user',)
        form = super(AccountAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        if obj is not None:
            obj.user = request.user
            obj.save()
