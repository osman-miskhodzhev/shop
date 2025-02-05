from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                'class': 'form-control py-4',
                'id': 'inputEmailAddress',
                'placeholder': 'Введите имя пользователя',
            }
        )
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                'class': 'form-control py-4',
                'id': 'inputPassword',
                'placeholder': 'Введите пароль',
                'type': 'password',
            }
        ),
    )
