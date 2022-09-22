from .models import Data
import django_filters

class DataFilter(django_filters.FilterSet):


    class Meta:
        model = Data
        fields = '__all__'