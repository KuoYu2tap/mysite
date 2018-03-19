# Create your views here.
from django.views.generic import ListView

from .models import Account


class AccountView(ListView):
    model = Account
    template_name = 'account/detail.html'
    context_object_name = 'accounts'

    # def get_queryset(self):
    #     res = self.model.objects.all()
    #     return res
    #
    # def get_context_data(self, **kwargs):
    #     res = self.model.objects.all()
    #     return res
