# order/admin.py

from django.contrib import admin
from .models import Order, OrderItem  # Import your Order model

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'updated_at')  # Customize the fields you want to display in the list view
    list_filter = ('status',)  # Add filters to the admin panel for easier management
    search_fields = ('id',)  # Add search functionality for the Order ID
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')  # Adjust the fields you want to display