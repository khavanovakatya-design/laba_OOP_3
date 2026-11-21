import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

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

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150, 
        required=True, 
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        # Добавляем новые поля в список
        fields = [
            'avatar', 'last_name', 'first_name', 'middle_name', 
            'phone', 'region', 'city', 'postal_code', 'address', 'bio'
        ]
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'style': 'padding: 10px;'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванович'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 000-00-00'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Московская область'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Москва'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123456'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Улица, дом, квартира'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Расскажите о себе...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(id=self.instance.user.id).exists():
            raise ValidationError("Этот логин уже занят. Выберите другой.")
        return username

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.user.username = self.cleaned_data['username']
            profile.user.save()
            profile.save()
        return profile