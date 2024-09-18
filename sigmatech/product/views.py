from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart, CartItem
from django.http import HttpResponseBadRequest

def catalog_view(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    category_id = request.GET.get('category', '')  # Get the selected category ID

    # Get all categories for the dropdown
    categories = Category.objects.all()

    # Filter products based on query and selected category
    products = Product.objects.all()

    # Apply search query if provided
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)  # Matches products under the searched category
        )

    # Apply category filtering if selected
    selected_category = None
    if category_id:
        try:
            selected_category = Category.objects.get(id=category_id)
            products = products.filter(category=selected_category)
        except Category.DoesNotExist:
            selected_category = None

    return render(request, 'product/catalog.html', {
        'categories': categories,
        'products': products,
        'query': query,  # Pass the query to the template for display
        'selected_category': selected_category,  # Pass selected category to the template
    })


def autocomplete(request):
    query = request.GET.get('term', '')  # Get the term being typed
    if query:
        # Search both category and product names
        categories = Category.objects.filter(name__icontains=query).values_list('name', flat=True)
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).values_list('name', flat=True)

        # Combine results and return suggestions
        suggestions = list(categories) + list(products)
        return JsonResponse(suggestions, safe=False)

    return JsonResponse([], safe=False)  # Return empty list if no query



@login_required(login_url='signin')
def add_to_cart(request, product_id):
    # Get the product by ID or return 404 if not found
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create the cart for the current user
    carts = Cart.objects.filter(user=request.user)
    
    if carts.exists():
        # Deactivate all carts for the user
        carts.update(active=False)
        # Get the latest cart (the one with the most recent created_at timestamp)
        cart = carts.latest('created_at')
        cart.active = True
        cart.save()
    else:
        # Create a new cart if none exists
        cart = Cart.objects.create(user=request.user, active=True)

    if request.method == 'POST':
        # Get the quantity from the form
        quantity = int(request.POST.get('quantity', 1))

        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            # Set the quantity for a new cart item
            cart_item.quantity = quantity
            messages.success(request, f"{product.name} added to your cart!")
        else:
            # Update the quantity if the product is already in the cart
            cart_item.quantity += quantity
            messages.success(request, f"{product.name} quantity updated in your cart!")
        
        # Save the cart item
        cart_item.save()

        # Redirect to the cart page or wherever appropriate
        return redirect('cart:cart')  # Assuming 'view_cart' is the URL name for the cart page
    
    else:
        # For GET requests, show the product details with default/pre-filled quantity
        quantity = request.GET.get('quantity', 1)

    return render(request, 'product/add_to_cart.html', {
        'product': product,
        'quantity': quantity,
    })
