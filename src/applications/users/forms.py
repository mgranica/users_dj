from django import forms
from django.contrib.auth import authenticate

from .models import User


class UserRegisterForm(forms.ModelForm):
    """Form definition for UserRegister."""

    password1 = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña"}),
    )

    password2 = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Repetir Contraseña"}),
    )

    class Meta:
        """Meta definition for UserRegisterform."""

        model = User
        fields = ("username", "email", "name", "last_names", "gender")

    def clean_password2(self):
        if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
            self.add_error("password2", "the password do not match")
        elif len(self.cleaned_data["password1"]) < 5:
            self.add_error(
                "password2", "the password needs to have more than 5 characters"
            )


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "username"}),
    )

    password1 = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña"}),
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password1']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('the user data is not correct')

        return self.cleaned_data

class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña actual"
                }
            )
    )
    password2 = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña nueva"
                }
            )
    )

class VerificationForm(forms.Form):
    code_registre = forms.CharField(required=True)

    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)
    def clean_code_registre(self):
        code = self.cleaned_data['code_registre']

        if len(code)==10:
            active = User.objects.code_validation(
                self.id_user,
                code
            )
            if not active:
                raise forms.ValidationError('the verification code is not correct')

        else:
            raise forms.ValidationError('the verification code is not correct')