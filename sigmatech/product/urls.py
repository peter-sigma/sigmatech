from django.contrib import admin
from django.urls import path
from .views import catalog_view, autocomplete

urlpatterns = [
    path('catalog/', catalog_view, name='catalog'),
    path('autocomplete/', autocomplete, name='autocomplete'),
]