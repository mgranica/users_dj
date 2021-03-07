from django import forms

from .models import User

class UserRegisterForm(forms.ModelForm):
    """Form definition for UserRegister."""

    class Meta:
        """Meta definition for UserRegisterform."""

        model = User
        fields = ('__all__')
