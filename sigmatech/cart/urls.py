from django.contrib import admin
from django.urls import path
from .views import view_cart, update_cart_item, remove_cart_item

urlpatterns = [
    path('cart/', view_cart, name='cart'),
    path('update_cart_item/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('remove_cart_item/<int:item_id>/', remove_cart_item, name='remove_cart_item'),
    # path('checkout/', checkout, name='checkout'),
]
