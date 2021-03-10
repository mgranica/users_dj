from django.shortcuts import render

from django.views.generic import (
    CreateView
)

from django.views.generic.edit import (
    FormView
)


from .forms import UserRegisterForm
from .models import User

# Create your views here.

class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            name=form.cleaned_data['name'],
            last_names=form.cleaned_data['last_names'],
            gender=form.cleaned_data['gender']
        )
        return super(UserRegisterView, self).form_valid(form)