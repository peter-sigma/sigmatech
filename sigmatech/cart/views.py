from django.shortcuts import render

# Create your views here.
from .models import Cart, CartItem
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_amount = sum(item.total_price() for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount
    }
    return render(request, 'cart/cart.html', context)


# cart/views.py


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