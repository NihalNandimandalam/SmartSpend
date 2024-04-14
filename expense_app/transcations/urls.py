from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("display", views.display, name='display'),
    path("category_chart", views.category_chart, name='category_chart'),
    path('new_transaction', views.new_transaction, name='new_transaction'),
    path('update_transaction/<str:pk>/', views.update_transaction, name='update_transaction'),
    path('delete_transaction/<str:pk>/', views.delete_transaction, name='delete_transaction'),
]