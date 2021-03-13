from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    View
)

from django.views.generic.edit import (
    FormView,
)


from .forms import (
    UserRegisterForm, 
    LoginForm, 
    UpdatePasswordForm
)
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

class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)

class LogoutView(View):
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )

class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/login.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('user_app:user-login')
    login_url = reverse_lazy('user_app:user-login')

    def form_valid(self, form):

        user = self.request.user
        user = authenticate(
            username=user.username,
            password=form.cleaned_data['password1']
        )
        if user:
            new_password = form.cleaned_data['password2']
            user.set_password(new_password)
            user.save()
        
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)
