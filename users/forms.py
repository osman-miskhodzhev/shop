import uuid
from datetime import timedelta

from django.utils.timezone import now

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UsernameField,
    UserCreationForm
)

from .models import CustomUser, EmailVerification


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

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
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
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control py-4',
                    'id': 'inputPassword',
                }
            ),
            'password2': forms.PasswordInput(
                attrs={
                    'class': 'form-control py-4',
                    'id': 'inputConfirmPassword',
                }
            ),
        }
    
    def save(self):
        user = super(UserRegistrationForm, self).save()
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(
            code=uuid.uuid4(),
            user=user,
            expiration=expiration
            )
        record.send_verification_mail()
        return user
        
