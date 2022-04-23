from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views as bookmarket_views

urlpatterns = [
    path('', bookmarket_views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='bookmarket/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='bookmarket/logout.html'), name='logout'),
    path('book/', bookmarket_views.book, name='book'),
    path('import/', bookmarket_views.imports, name='import'),
    path('bill/', bookmarket_views.bill, name='bill'),
]
