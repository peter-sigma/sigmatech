from django.contrib import admin
from django.urls import path
from .views import *


app_name = 'dashboard'

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
]