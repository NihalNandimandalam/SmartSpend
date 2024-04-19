from django.contrib import admin
from .models import Balance, Customer, Statements

# Register your models here.
admin.site.register(Balance)
admin.site.register(Customer)
admin.site.register(Statements)