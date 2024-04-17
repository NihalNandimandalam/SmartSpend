import django_filters
from django_filters import DateFilter

from .models import *

class TransactionFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="transaction_date", lookup_expr='gte',label='start_date')
    end_date = DateFilter(field_name="transaction_date", lookup_expr='lte', label='end_date')
    class Meta:
        model = Balance
        fields = '__all__'
        exclude = ['transaction_date']
