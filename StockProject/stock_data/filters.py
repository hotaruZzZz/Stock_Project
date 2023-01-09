from .models import Data, Stock, Focus
import django_filters

class DataFilter(django_filters.FilterSet):


    class Meta:
        model = Data
        fields = '__all__'

class StockFilter(django_filters.FilterSet):


    class Meta:
        model = Stock
        fields = '__all__'

class FocusFilter(django_filters.FilterSet):


    class Meta:
        model = Focus
        fields = '__all__'