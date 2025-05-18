from django import forms
from .models  import *




class LoginForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'id':'login', 'class':'login'}), max_length=65, label="Логин")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'password'}), label="Пароль")

    



class AdForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'] = forms.CharField(min_length=2, max_length=80, label='Название')
        self.fields['description'] = forms.CharField(label="Описание")
        self.fields['image_url'] = forms.CharField(label="Ссылка на изображение")
        self.fields['category'] = forms.CharField(label="Категория")
        self.fields['condition'] = forms.CharField(label="Состояние")
        # self.fields['created_at'] = forms.HiddenInput()
        # self.fields['user'] = forms.HiddenInput()

    class Meta:
        model = Ad
        fields = ['title', 'user', 'description', 'image_url', 'category', 'condition', 'created_at']




    def set_ad(self, ad):
        self.fields['title'].initial = ad.title
        self.fields['description'].initial = ad.description
        self.fields['image_url'].initial = ad.image_url
        self.fields['category'].initial = ad.category
        self.fields['condition'].initial = ad.condition