from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    class Meta:
        db_table='customer'

class Statements(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    monthly_statement = models.FileField(upload_to='documents/' , null=True)
    def save(self, *args, **kwargs):
        # Append customer_id to the document name
        print(self.customer)
        filename = f"{self.monthly_statement.name}_{self.customer_id}"
        self.monthly_statement.name = filename
        super().save(*args, **kwargs)
    class Meta:
        db_table='statements'

class Balance(models.Model):
    CATEGORY = (
        ('Food', 'Food'),
        ('Investment', 'Investment'),
        ('Medical', 'Medical'),
        ('Miscellaneous', 'Miscellaneous'),
        ('Rent','Rent'),
        ('Grocery','Grocery'),
        ('Entertainment','Entertainment'),
        ('Bills','Bills')
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
    def _str_(self):
        return self.transaction_description
    class Meta:
        db_table='transactions'
