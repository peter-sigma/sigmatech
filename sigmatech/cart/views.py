from django.shortcuts import render, redirect
from django.core.exceptions import MultipleObjectsReturned

# Create your views here.
from .models import Cart, CartItem
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
import paypalrestsdk
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from order.models import Order, OrderItem

@login_required(login_url='signin')
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user, active=True)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user, active=True)
    except MultipleObjectsReturned:
        carts = Cart.objects.filter(user=request.user, active=True)
        cart = carts.first()
        carts.exclude(id=cart.id).update(active=False)

    if request.method == 'POST' and 'checkout' in request.POST:
        existing_order = Order.objects.filter(cart=cart).first()
        
        if existing_order:
            # Redirect to the order list if an order already exists for this cart
            return redirect('order:order_list')
        else:
            order = Order.objects.create(
                user=request.user,
                cart=cart,
                status='pending'
            )
            
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                )
            
            cart.items.all().delete()
            cart.active = False
            cart.save()
            
            new_cart = Cart.objects.create(user=request.user, active=True)
            
            return redirect('order:order_list')

    cart_items = cart.items.all()
    total_amount = sum(item.total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'cart/cart.html', context)



@require_POST
def update_cart_item(request, item_id):
    # Get the quantity from the request
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        # Get the cart item
        item = CartItem.objects.get(id=item_id)
        item.quantity = quantity
        item.save()
        # Return success response with updated total price
        return JsonResponse({
            'success': True,
            'item_total': item.total_price()
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'})


@require_POST
def remove_cart_item(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id)
        item.delete()
        return JsonResponse({'success': True})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'})
    

