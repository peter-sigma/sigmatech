from django.shortcuts import render, redirect

# Create your views here.
from .models import Cart, CartItem
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
import paypalrestsdk
from django.conf import settings
from django.urls import reverse

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
    

# Configure PayPal SDK with credentials
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def create_payment(request):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/cart/payment/execute",
            "cancel_url": "http://localhost:8000/cart/payment/cancel"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Item Name",
                    "sku": "item",
                    "price": "10.00",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "10.00",
                "currency": "USD"
            },
            "description": "Payment description"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                return redirect(link.href)  # Redirect to PayPal for payment approval
    else:
        return JsonResponse({'error': 'Error in creating payment'})
    


  
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'cart/payment_success.html')
    else:
        return render(request, 'cart/payment_failed.html')


def cancel_payment(request):
    # You can redirect the user back to the cart or a cancellation page
    return redirect('cart')