from django.forms import ModelForm, widgets
from .models import Balance

class TransactionForm(ModelForm):
    class Meta:
        model = Balance
        exclude = ('customer',)
        fields = '__all__'
        widgets = {
            'transaction_date': widgets.DateInput(attrs={'type':'date'})
        }
