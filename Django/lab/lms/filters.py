import django_filters 
from django_filters import *
from .models import *


class JournalFilter(django_filters.FilterSet):
    client_name = django_filters.CharFilter(lookup_expr='icontains')
    client_surname = django_filters.CharFilter(lookup_expr='icontains')
    birth = django_filters.DateFromToRangeFilter() 
    analysis_name = django_filters.ModelMultipleChoiceFilter(queryset=Price.objects.all())
    analysis_cathegory = django_filters.ModelMultipleChoiceFilter(queryset=Structure.objects.all())
    date_time = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model= Journal 
        fields =['date_time', 'client_name', 'client_surname', 'client_phone', 'sex', 'birth', 'analysis_name', 'analysis_cathegory', 'is_done' ]
        
        
        
        