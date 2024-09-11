from django.contrib import admin
from django.urls import path
from .views import catalog_view

urlpatterns = [
    path('catalog/', catalog_view, name='catalog'),
]