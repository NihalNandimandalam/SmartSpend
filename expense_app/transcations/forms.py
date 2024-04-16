from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Balance, Statements

class TransactionForm(ModelForm):
    class Meta:
        model = Balance
        exclude = ('customer',)
        fields = '__all__'
        widgets = {
            'transaction_date': widgets.DateInput(attrs={'type':'date'})
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UploadFileForm(ModelForm):
    class Meta:
        model = Statements
        fields = "__all__"
        exclude = ('customer',)
    # file = forms.FileField()