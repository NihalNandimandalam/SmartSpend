from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import Balance, Statements
from django.db.models.functions import TruncMonth,TruncYear
from django.db.models import F,Q, Sum
from .forms import TransactionForm

import pandas as pd
import numpy as np
import yfinance as yahooFinance

def index(request):
    return HttpResponse("Hello, world. You're at the View index.")

def display(request):  
    # dateFilter = TransactionFilter(request.GET, queryset=transactions_list)
    # transactions_list = dateFilter.qs
    if request.method == 'POST':
        user_loggedin = request.user.customer
        customer_list = Balance.objects.filter(customer = user_loggedin)
        unique_months = customer_list.annotate(month_year=TruncMonth(F('transaction_date'))).values_list('month_year', flat=True).distinct()
        unique_years = customer_list.annotate(month_year=TruncYear(F('transaction_date'))).values_list('month_year', flat=True).distinct()
        unique_month_list = [i.month for i in unique_months]
        unique_year_list = [i.year for i in unique_years]
        month = [request.POST.get('month_view')]
        year = [request.POST.get('year_view')]
        tag = request.POST.get('tag')
        if tag=="Income":
            customer_list = customer_list.filter(tag="Income")
        elif tag=="Expense":
            customer_list = customer_list.filter(tag="Expense")
        if month == ['all']:
            month = unique_month_list
        if year == ['all']:
            year = unique_year_list
        category_list = customer_list.values_list('category', flat=True).distinct()
        category_list = [i for i in category_list]
        filtered_category = [request.POST.get('category')]
        if filtered_category == ['all']:
            filtered_category = category_list
        transactions_list = customer_list.filter(Q(transaction_date__month__in=month)&Q(transaction_date__year__in=year)&Q(category__in=filtered_category)).order_by('transaction_date')
        
        print(category_list,filtered_category)
        try:
            income = round(transactions_list.filter(tag="income").aggregate(Sum("amount"))["amount__sum"],2)
        except TypeError:
            income = transactions_list.filter(tag="income").aggregate(Sum("amount"))["amount__sum"]
        
        try:
            expense = round(transactions_list.filter(tag="expense").aggregate(Sum("amount"))["amount__sum"],2)
        except TypeError:
            expense = transactions_list.filter(tag="expense").aggregate(Sum("amount"))["amount__sum"]
        return render(request,"transcations/display.html",
                  {"transactions_list":transactions_list,'unique_months':unique_month_list, 'unique_years':unique_year_list,
                   "income":income, "expense":expense,"selected_month":month[0],"selected_year":year[0],"selected_tag":tag,
                   "category_list":category_list,"selected_category":filtered_category})
    else:
        user_loggedin = request.user.customer
        customer_list = Balance.objects.filter(customer = user_loggedin)

        unique_months = customer_list.annotate(month_year=TruncMonth(F('transaction_date'))).values_list('month_year', flat=True).distinct()
        unique_years = customer_list.annotate(month_year=TruncYear(F('transaction_date'))).values_list('month_year', flat=True).distinct()
        transactions_list = customer_list.all().order_by('transaction_date')
        unique_month_list = [i.month for i in unique_months]
        unique_year_list = [i.year for i in unique_years]
        category_list = customer_list.values_list('category', flat=True).distinct()
        category_list = [i for i in category_list]
        income = round(transactions_list.filter(tag="income").aggregate(Sum("amount"))["amount__sum"],2)
        expense = round(transactions_list.filter(tag="expense").aggregate(Sum("amount"))["amount__sum"],2)
        return render(request,"transcations/display.html",
                    {"transactions_list":transactions_list,"unique_months":unique_month_list, "unique_years":unique_year_list,
                     "income":income, "expense":expense,"category_list":category_list})

def new_transaction(request):
    form = TransactionForm()
    display_text = "Add new transaction"
    if request.method == 'POST':
        form = TransactionForm(request.POST)        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.customer = request.user.customer
            instance.save()
            return redirect('display')
    return render(request,"transcations/new_transaction.html",{"form":form, "display_text":display_text})

def update_transaction(request, pk):
    transaction = Balance.objects.get(transaction_id=pk)
    form = TransactionForm(instance=transaction)
    display_text = "Edit transaction"
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('display')
    return render(request,"transcations/new_transaction.html",{"form":form, "display_text":display_text})


def delete_transaction(request, pk):
    transaction = Balance.objects.get(transaction_id=pk)
    if request.method =="POST":
        transaction.delete()
        return redirect('display')
    return render(request, "transcations/delete.html",{"transaction":transaction})

def category_chart(request):
    user_loggedin = request.user.customer
    customer_list = Balance.objects.filter(customer = user_loggedin)

    unique_months = customer_list.annotate(month_year=TruncMonth(F('transaction_date'))).values_list('month_year', flat=True).distinct()
    unique_years = customer_list.annotate(month_year=TruncYear(F('transaction_date'))).values_list('month_year', flat=True).distinct()
    unique_month_list = [i.month for i in unique_months]
    unique_year_list = [i.year for i in unique_years]
    tag = "Expense" #default expense tag
    if request.method=='POST':
        month = [request.POST.get('month_view')]
        year = [request.POST.get('year_view')]
        tag = request.POST.get('tag')
        if tag=="Income":
            customer_list = customer_list.filter(tag="Income")
        elif tag=="Expense":
            customer_list = customer_list.filter(tag="Expense")
        if month == ['all']:
            month = unique_month_list
        if year == ['all']:
            year = unique_year_list
        transactions_list = customer_list.filter(Q(transaction_date__month__in=month)&Q(transaction_date__year__in=year)).order_by('transaction_date')
        try:
            income = round(transactions_list.filter(tag="income").aggregate(Sum("amount"))["amount__sum"],2)
        except TypeError:
            income = transactions_list.filter(tag="income").aggregate(Sum("amount"))["amount__sum"]
        
        try:
            expense = round(transactions_list.filter(tag="expense").aggregate(Sum("amount"))["amount__sum"],2)
        except TypeError:
            expense = transactions_list.filter(tag="expense").aggregate(Sum("amount"))["amount__sum"]
    else:
        transactions_list = customer_list.all().order_by('transaction_date')
        income = round(transactions_list.filter(tag="income").aggregate(Sum("amount"))["amount__sum"],2)
        expense = round(transactions_list.filter(tag="expense").aggregate(Sum("amount"))["amount__sum"],2)
    label = []
    data = []
    for c in transactions_list.values('category').annotate(total_price=Sum('amount')).order_by('category'):
        print(c)
        label.append(c['category'])
        data.append(c['total_price'])
    category_df = pd.DataFrame({
        'category':label,
        'total_amount':data,
    })
    category_df = category_df.sort_values(by=['total_amount'],ascending=False)
    return render(request, "transcations/category_chart.html",
                  {'labels':label, 'data':data,"unique_months":unique_month_list, "unique_years":unique_year_list,
                   "selected_tag":tag,"Income":income,"Expense":expense,"category_df":category_df})


def finance_page(request):
    user_loggedin = request.user.customer
    customer_list = Balance.objects.filter(customer = user_loggedin)

    unique_months = customer_list.annotate(month_year=TruncMonth(F('transaction_date'))).values_list('month_year', flat=True).distinct()
    unique_years = customer_list.annotate(month_year=TruncYear(F('transaction_date'))).values_list('month_year', flat=True).distinct()
    unique_month_list = [i.month for i in unique_months]
    unique_year_list = [i.year for i in unique_years]
    if request.method=='POST':
        month = [request.POST.get('month_view')]
        year = [request.POST.get('year_view')]
        if month == ['all']:
            month = unique_month_list
        if year == ['all']:
            year = unique_year_list
        transactions_list = customer_list.filter(Q(transaction_date__month__in=month)&Q(transaction_date__year__in=year)).order_by('transaction_date')
    else:
        transactions_list = customer_list.all().order_by('transaction_date')
    
    try:
        income = round(transactions_list.filter(tag="income").aggregate(Sum("amount"))["amount__sum"],2)
    except TypeError:
        income = transactions_list.filter(tag="income").aggregate(Sum("amount"))["amount__sum"]
    
    try:
        expense = round(transactions_list.filter(tag="expense").aggregate(Sum("amount"))["amount__sum"],2)
    except TypeError:
        expense = transactions_list.filter(tag="expense").aggregate(Sum("amount"))["amount__sum"]
    try:
        savings = round(income - expense,2)
    except TypeError:
        savings = 0
    if savings>0:
        tag = "positive"
    else: 
        tag = "negative"
    stocks_df = get_share_prices()
    stocks_df['earnings'] = (stocks_df['return_yearly']/100) * (abs(savings) *0.1)
    stocks_df['earnings'] = stocks_df['earnings'].round(2)
    if tag == "positive":
        stocks_df['total_saving'] = abs(savings)+stocks_df['earnings']
    else:
        stocks_df['total_saving'] = stocks_df['earnings']
    stocks_df['total_saving'] = stocks_df['total_saving'].round(2)
    return render(request, "transcations/finance_page.html",
                  {"unique_months":unique_month_list, "unique_years":unique_year_list,
                   "income":income,"expense":expense,"savings":savings, "stocks_df":stocks_df,"tag":tag,})


def get_share_prices():
    symbols = ['^GSPC','^IXIC','META','AMZN','GOOG','FBGRX']
    return_daily, return_monthly ,return_yearly = [], [], []
    for symbol in symbols:
        GetInformation = yahooFinance.Ticker(symbol)
        share = GetInformation.history(period="10y")
        return_daily.append(share['Close'].pct_change().mean())
        return_monthly.append(share['Close'].resample('M').ffill().pct_change().mean())
        return_yearly.append(round(share['Close'].resample('Y').ffill().pct_change().mean()*100,2))
    
    share_name = ['S&P500','NASDAQ']+symbols[2:]
    stock_df = pd.DataFrame({
        'share_name':share_name,
        # 'return_daily':return_daily,
        # 'return_monthly':return_monthly,
        'return_yearly':return_yearly,
    })   
    return stock_df
