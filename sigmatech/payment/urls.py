from django.contrib import admin
from django.urls import path
from .views import create_payment, execute_payment, cancel_payment

app_name = 'payment'
urlpatterns = [
    path('create_payment/', create_payment, name='create_payment'),
    path('execute_payment/', execute_payment, name='execute_payment'),
    path('payment/execute/', execute_payment, name='execute_payment'),
    path('payment/cancel/', cancel_payment, name='cancel_payment'),
]