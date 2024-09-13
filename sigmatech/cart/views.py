from django.shortcuts import render

# Create your views here.
from .models import Cart, CartItem

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_amount = sum(item.total_price for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount
    }
    return render(request, 'cart/cart.html', context)
