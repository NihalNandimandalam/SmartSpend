from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    class Meta:
        db_table='customer'


class Balance(models.Model):
    CATEGORY = (
        ('Food', 'Food'),
        ('Investment', 'Investment'),
        ('Medical', 'Medical'),
        ('Miscellaneous', 'Miscellaneous')
    )
    TAG = (
        ('Income', 'Income'),
        ('Expense', 'Expense')
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    transaction_id = models.AutoField(primary_key=True)
    transaction_date = models.DateField()
    transaction_description = models.CharField(max_length=200)
    amount = models.FloatField()
    category = models.CharField(max_length=200, choices=CATEGORY)
    tag = models.CharField(max_length=50, choices=TAG)
    def __str__(self):
        return self.transaction_description
    class Meta:
        db_table='transactions'
