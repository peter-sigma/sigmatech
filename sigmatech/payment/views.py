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
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags



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



def send_order_email(order, status, user=None):
    """Send email based on payment success or failure."""
    if status == 'success':
        subject = f'Order {order.id} - Payment Successful'
        template = 'emails/payment_success.html'
        context = {
            'username': order.user.username,
            'order_number': order.id,
            'order_date': order.created_at,
            'total_amount': order.total_price,
        }
    elif status == 'failed':
        subject = 'Payment Failed - Please Try Again'
        template = 'emails/payment_failed.html'
        context = {'user': user}

    # Generate HTML and plain text versions of the email
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = order.user.email if order else user.email

    send_mail(
        subject,
        plain_message,
        from_email,
        [to_email],
        html_message=html_message
    )


  
@login_required(login_url='user:signin')
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Payment successful - Update order status and clear cart
        cart = Cart.objects.filter(user=request.user, active=True).first()
        if not cart:
            return render(request, 'payment/payment_failed.html', {'error': 'No active cart found.'})

        try:
            order = Order.objects.get(user=request.user, cart=cart, status='pending')
        except Order.DoesNotExist:
            return render(request, 'payment/payment_failed.html', {'error': 'No pending order found for this cart.'})

        # Calculate total price from cart items
        total_price = 0
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            total_price += cart_item.product.price * cart_item.quantity
            
        # Create OrderItems and adjust stock
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            product = cart_item.product
            if product.quantity >= cart_item.quantity:
                product.quantity -= cart_item.quantity
                product.save()
            else:
                return render(request, 'payment/payment_failed.html', {'error': f'Insufficient stock for {product.name}'})

        # Set the total price in the order
        order.total_price = total_price
        order.status = 'processing'
        order.save()

        # Clear the cart
        cart.items.all().delete()
        Cart.objects.create(user=request.user, active=True)

        # Send Success Email
        send_order_email(order, 'success')

        return render(request, 'payment/payment_success.html', {'order': order})
    else:
        # Send Failure Email
        send_order_email(order=None, status='failed', user=request.user)

        return render(request, 'payment/payment_failed.html', {'error': 'Payment execution failed.'})

def cancel_payment(request):
    # You can redirect the user back to the cart or a cancellation page
    return redirect('cart:cart')
