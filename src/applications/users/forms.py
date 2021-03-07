from django import forms

from .models import User

class UserRegisterForm(forms.ModelForm):
    """Form definition for UserRegister."""

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )

    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña'
            }
        )
    )
    
    class Meta:
        """Meta definition for UserRegisterform."""

        model = User
        fields = (
            'username',
            'email',
            'name',
            'last_names',
            'gender'
        )
