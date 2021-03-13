import datetime
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    TemplateView
)

# Create your views here.

class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "home/index.html"
    login_url = reverse_lazy('user_app:user-login')


class DateMixin(object):

    def get_context_data(self, **kwargs):
        context = super(DateMixin, self).get_context_data(**kwargs)
        context['date'] = datetime.datetime.now()
        return context
    
class TestMixin(DateMixin, TemplateView):
    template_name = "home/mixin.html"
    