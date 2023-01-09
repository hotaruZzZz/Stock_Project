from django import forms
from django.utils.translation import gettext_lazy as _ # 新增
from .models import Data
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = '__all__'
        labels = {
            'sName': _('股票名稱'),
            'sNumber' : _('股票代號'),
            'sDate' : _('日期'),
            'sOpen' : _('開盤'),
            'sHigh' : _('最高'),
            'sLow' : _('最低'),
            'sClose' : _('收盤'),
        }
        
class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')