from django.contrib.auth.forms import UserCreationForm
from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput
from django.contrib.auth.models import User


# class CustomCaptchaForm(CaptchaTextInput):
#     template_name = 'custom_field.html'


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(widget=CaptchaTextInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')