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
        fields = ['title', 'description', 'image_url', 'category', 'condition']




    def set_ad(self, ad):
        self.fields['title'].initial = ad.title
        self.fields['description'].initial = ad.description
        self.fields['image_url'].initial = ad.image_url
        self.fields['category'].initial = ad.category
        self.fields['condition'].initial = ad.condition


class CommentForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [('Ожидает', 'Ожидает'),('Принята', 'Принята'),('Отклонена', 'Отклонена')]
        self.fields['comment'] = forms.CharField(label="Коментарий")
        # self.fields['status'] = forms.ChoiceField(
        #     label="Статус", 
        #     choices = choices,
        #     initial = choices[0],
        #     disabled = True
        #     )

        self.fields['ad_receiver'] = forms.ModelChoiceField(
            label='Предложить', 
            queryset=Ad.objects.filter(user=user, is_bonded=False), 
            empty_label='Не выбрано'
            )



    class Meta:
        model = ExchangeProposal
        fields = ['comment', 'ad_receiver']