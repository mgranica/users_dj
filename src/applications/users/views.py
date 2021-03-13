from django.shortcuts import render
from django.core.mail import send_mail
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
    UpdatePasswordForm,
    VerificationForm,
)
from .models import User
from .functions import code_generator

# Create your views here.

class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        code = code_generator()
        user = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            name=form.cleaned_data['name'],
            last_names=form.cleaned_data['last_names'],
            gender=form.cleaned_data['gender'],
            register_code= code
        )
        # send mail with the code
        subject = 'mail confirmation'
        message = 'Verification code: ' + code
        sender_email = 'migue.granica@gmail.com'

        send_mail(subject, message, sender_email, [form.cleaned_data['email'],])
        # redirect to validation screen
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification'
            )
        )

class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user_item = authenticate(
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
                'users_app:user-login',
                kwargs={'pk': user_item.id}
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

class CodeVerification(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('home_app:user-login')

    def get_form_kwargs(self):
        kwargs = super(CodeVerification, self).get_form_kwargs()
        kwargs.update({
            'pk':self.kwargs['pk'],
        })
        return kwargs

    def form_valid(self, form):
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )
        return super(CodeVerification, self).form_valid(form)