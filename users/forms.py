from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from .models import CustomUser


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


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'profile_image',
            'username',
            'email'
        ]
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control py-4',
                    'id': 'inputFirstName',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control py-4',
                    'id': 'inputLastName',
                }
            ),
            'profile_image': forms.FileInput(
                attrs={
                    'class': 'custom-file-input',
                    'id': 'userAvatar',
                    'size': '50',
                    'type': 'file',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control py-4',
                    'id': 'inputUsername',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control py-4',
                    'id': 'inputEmailAddress',
                }
            ),
        }
