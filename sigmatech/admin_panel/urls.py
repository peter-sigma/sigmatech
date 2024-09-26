from django.contrib import admin
from django.urls import path
from .views import *


app_name = 'admin_panel'

urlpatterns = [
    path('login/', admin_login, name='admin_login'),
    
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('products/', admin_manage_products, name='admin_manage_products'),
    path('orders/', admin_manage_orders, name='admin_manage_orders'),
    path('users/', admin_manage_users, name='admin_manage_users'),
    path('settings/', admin_settings, name='admin_settings'),
    path('help/', admin_help, name='admin_help'),
    
    
    path('order/view/<int:order_id>/', view_order, name='view_order'),
     path('order/<int:order_id>/update-status/', admin_update_order_status, name='admin_update_order_status'),
    
    
    path('products/add/', admin_add_product, name='admin_add_product'),
    path('products/edit/<int:product_id>/', admin_edit_product, name='admin_edit_product'),
    path('products/delete/<int:product_id>/', admin_delete_product, name='admin_delete_product'),
    
    path('categories/', admin_manage_categories, name='admin_manage_categories'),
    path('categories/add/', admin_add_category, name='admin_add_category'),
    path('categories/edit/<int:category_id>/', admin_edit_category, name='admin_edit_category'),
    path('categories/delete/<int:category_id>/', admin_delete_category, name='admin_delete_category'),
    
    path('order/<int:order_id>/', admin_view_order, name='admin_view_order'),
    
     

]