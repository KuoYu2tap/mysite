from django.contrib import admin

from .models import Account


# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    date_hierarchy = 'spent_date'
    list_filter = ('reason',)
    list_per_page = 20
    list_display = ('reason', 'cost')

    def get_queryset(self, request):
        qs = super(AccountAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
