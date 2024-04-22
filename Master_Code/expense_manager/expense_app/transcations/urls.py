from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("about", views.about, name="about"),
    path("services", views.services, name="services"),
    path("team", views.team, name="team"),
    path("contact", views.contact, name="contact"),
    path("display", views.display, name='display'),
    path("login", views.login_page, name='login'),
    path("logout", views.logoutUser, name='logout'),
    path("register", views.register_page, name='register'),
    path("user", views.user_page, name='user_page'),
    path("category_chart", views.category_chart, name='category_chart'),
    path("finance_page", views.finance_page, name='finance_page'),
    path("loan_page", views.loan_page, name='loan_page'),
    path('new_transaction', views.new_transaction, name='new_transaction'),
    path('update_transaction/<str:pk>/', views.update_transaction, name='update_transaction'),
    path('delete_transaction/<str:pk>/', views.delete_transaction, name='delete_transaction'),
    path("upload", views.upload_page, name='upload'),
]