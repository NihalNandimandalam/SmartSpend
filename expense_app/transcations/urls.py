from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("display", views.display, name='display'),
    path("category_chart", views.category_chart, name='category_chart'),
    path("finance_page", views.finance_page, name='finance_page'),
    path("loan_page", views.loan_page, name='loan_page'),
    path('new_transaction', views.new_transaction, name='new_transaction'),
    path('update_transaction/<str:pk>/', views.update_transaction, name='update_transaction'),
    path('delete_transaction/<str:pk>/', views.delete_transaction, name='delete_transaction'),
    path("upload", views.upload_page, name='upload'),
]