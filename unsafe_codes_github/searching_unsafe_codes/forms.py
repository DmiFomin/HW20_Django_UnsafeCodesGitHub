from django import forms
from .models import Settings


class SettingsForm(forms.ModelForm):
    author = forms.CharField(label = 'Автор')
    phone = forms.CharField(label = 'Телефон')
    email = forms.EmailField(label = 'E-mail')
    class Meta:
        model = Settings
        #fields = '__all__'
        #fields = ('author', 'phone', 'email')
        exclude = ('path_to_token',)



