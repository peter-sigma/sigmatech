from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from order.models import Order, OrderItem
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import paypalrestsdk
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned



# Configure PayPal SDK with credentials
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


@login_required
def create_payment(request):
    # Ensure the cart is active and associated with the user
    try:
        cart = Cart.objects.get(user=request.user, active=True)
    except Cart.DoesNotExist:
        return redirect('cart:cart')  # Redirect if no active cart exists

    # Get all items from the cart
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in cart_items)

    # Check if an existing pending order exists for this cart
    existing_order = Order.objects.filter(cart=cart, status='pending').first()

    if existing_order:
        order = existing_order
    else:
        # Create a new order if none exists
        order = Order.objects.create(user=request.user, cart=cart, status='pending')

    # No OrderItem creation here, only after payment execution.

    # Create the PayPal payment
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/payment/payment/execute",
            "cancel_url": "http://localhost:8000/payment/payment/cancel"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Cart Items",
                    "sku": "cart",
                    "price": str(total),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(total),
                "currency": "USD"
            },
            "description": "Payment for cart items"
        }]
    })

    if payment.create():
        # Redirect to PayPal for payment approval
        for link in payment.links:
            if link.method == "REDIRECT":
                return redirect(link.href)
    else:
        return JsonResponse({'error': 'Error in creating payment'})






  
@login_required



def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    # Find the payment in PayPal
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Payment successful - Update order status and clear cart
        
        # Fetch the latest active cart for the user
        cart = Cart.objects.filter(user=request.user, active=True).first()
        if not cart:
            return render(request, 'payment/payment_failed.html', {'error': 'No active cart found.'})
        
        # Try to fetch the pending order associated with this cart
        try:
            order = Order.objects.get(user=request.user, cart=cart, status='pending')
        except Order.DoesNotExist:
            return render(request, 'payment/payment_failed.html', {'error': 'No pending order found for this cart.'})
        
        # Create OrderItems from CartItems
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Update the order status to 'processing'
        order.status = 'processing'
        order.save()

        # Clear all items in the cart
        cart.items.all().delete()

        # Create a new active cart for the user
        Cart.objects.create(user=request.user, active=True)

        # Render success page
        return render(request, 'payment/payment_success.html', {'order': order})
    else:
        # Payment failed, show failure page
        return render(request, 'payment/payment_failed.html', {'error': 'Payment execution failed.'})



def cancel_payment(request):
    # You can redirect the user back to the cart or a cancellation page
    return redirect('cart:cart')
