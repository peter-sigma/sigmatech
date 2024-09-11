from django.contrib import admin

# Register your models here.
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')  # Adjust the fields you want to display
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'image')  # Adjust the fields you want to display
    list_filter = ('category',)
    search_fields = ('name', 'category__name')  # Search by product name and category name