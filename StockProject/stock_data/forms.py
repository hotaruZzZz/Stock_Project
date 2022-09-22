from django import forms
from django.utils.translation import gettext_lazy as _ # 新增
from .models import Data

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
        