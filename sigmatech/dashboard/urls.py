from django.contrib import admin
from django.urls import path
from .views import *


app_name = 'dashboard'

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/products/', admin_manage_products, name='admin_manage_products'),
    path('dashboard/admin/orders/', admin_manage_orders, name='admin_manage_orders'),
    path('dashboard/admin/customers/', admin_manage_users, name='admin_manage_users'),
    path('dashboard/admin/settings/', admin_settings, name='admin_settings'),
    path('dashboard/admin/help/', admin_help, name='admin_help'),
]