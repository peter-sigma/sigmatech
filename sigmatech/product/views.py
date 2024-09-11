from django.shortcuts import render
from .models import Category, Product

def catalog_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'product/catalog.html', {
        'categories': categories,
        'products': products,
    })
