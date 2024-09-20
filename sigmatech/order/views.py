from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order
from cart.models import Cart

# Create your views here.
def hello_world_view(request):
    return render(request, 'order/hello.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from order.models import Order, OrderItem

@login_required(login_url='user:signin')
def order_list(request):
    # Ensure the user has exactly one active cart
    cart = Cart.objects.filter(user=request.user, active=True).first()
    if not cart:
        # If no active cart exists, create a new one
        cart = Cart.objects.create(user=request.user, active=True)
    
    # Fetch all orders for the user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Calculate and save the total price for each order
    for order in orders:
        total_price = sum(item.price * item.quantity for item in order.items.all())
        order.total_price = total_price
        order.save()  # Save the updated total price to the database
    
    # Pass the orders to the template
    context = {
        'orders': orders,  # Pass all orders directly
    }
    
    return render(request, 'order/order.html', context)