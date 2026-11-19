import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[\w.@+-]+$', username, re.UNICODE):
            raise ValidationError("Логин может содержать только буквы, цифры и символы @/./+/-/_")
        return username

class LoginForm(AuthenticationForm):
    pass

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

class PasswordResetConfirmForm(forms.Form):
    code = forms.CharField(label="Код из письма", max_length=4)
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return cleaned_data