from django import forms
from .models  import *




class LoginForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'id':'login', 'class':'login'}), max_length=65, label="Логин")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'password'}), label="Пароль")

    