from django.contrib import admin
from django.urls import path
from .views import catalog_view, autocomplete, add_to_cart

urlpatterns = [
    path('catalog/', catalog_view, name='catalog'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

]