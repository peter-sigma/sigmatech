from django.contrib import admin
from .models import Cart, CartItem

# Registering Cart model
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']
    list_filter = ['created_at']

# Registering CartItem model
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    search_fields = ['cart__user__username', 'product__name']
    list_filter = ['cart__created_at']

