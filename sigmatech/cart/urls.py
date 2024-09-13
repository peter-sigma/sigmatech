from django.contrib import admin
from django.urls import path
from .views import view_cart

urlpatterns = [
    path('cart/', view_cart, name='cart'),
    # path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    # path('checkout/', checkout, name='checkout'),
]
