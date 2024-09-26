from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from order.models import Order
from django.shortcuts import render, get_object_or_404, redirect
from product.models import Category, Product
from product.forms import CategoryForm, ProductForm
from dashboard.forms import OrderStatusForm
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def admin_only(user):
    return user.is_superuser


def admin_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    messages.success(request, f"Welcome back, {username}!")
                    
                    # Redirect to the 'next' URL or the admin dashboard
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('admin_panel:admin_dashboard')
                else:
                    messages.error(request, "Access restricted to admin users.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = AuthenticationForm()

    return render(request, 'admin_panel/admin_login.html', {'form': form})




@user_passes_test(admin_only)
def admin_dashboard(request):
    return render(request, 'admin_panel/admindashboard.html')


# Display all products
@user_passes_test(admin_only)
def admin_manage_products(request):
    products = Product.objects.all()
    return render(request, 'admin_panel/manage_products.html', {'products': products})

# Add new product
@user_passes_test(admin_only)
def admin_add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:admin_manage_products')
    else:
        form = ProductForm()
    return render(request, 'admin_panel/add_product.html', {'form': form})

# Edit product
@user_passes_test(admin_only)
def admin_edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:admin_manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_panel/edit_product.html', {'form': form, 'product': product})

# Delete product
@user_passes_test(admin_only)
def admin_delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_panel:admin_manage_products')
    return render(request, 'admin_panel/delete_product.html', {'product': product})

# Manage categories
@user_passes_test(admin_only)
def admin_manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'admin_panel/manage_categories.html', {'categories': categories})

# Add new category
@user_passes_test(admin_only)
def admin_add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:admin_manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'admin_panel/add_category.html', {'form': form})

# View to edit an existing category
@login_required(login_url='user:signin')
def admin_edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('admin_panel:admin_manage_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin_panel/edit_category.html', {
        'form': form,
        'category': category
    })

# View to delete a category
@login_required(login_url='user:signin')
def admin_delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('admin_panel:admin_manage_categories')
    return render(request, 'admin_panel/delete_category.html', {
        'category': category
    })
    
    
@user_passes_test(admin_only)
def admin_manage_orders(request):
     # Retrieve all orders
    orders = Order.objects.all().order_by('-created_at')  # Latest orders first
    for order in orders:
        total_price = sum(item.price * item.quantity for item in order.items.all())
        order.total_price = total_price
        order.save()  # Save the updated total price to the database
    # Calculate and save the total price for each order (if needed)

    context = {
        'orders': orders,
    }
    return render(request, 'admin_panel/manage_orders.html', context)


# Admin view to display order details
@user_passes_test(admin_only)
def admin_view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Fetch the specific order by ID
    order_items = order.items.all()  # Get all items related to the order
    # Calculate the total price by summing the total for each order item
    total_price = sum(item.total_price() for item in order_items)
    print(total_price)
    context = {
        'order': order,
        'order_items': order_items,  # Pass order items to the template
        'total_price': total_price,  # Pass the total price to the template
    }
    return render(request, 'admin_panel/order_detail.html', context)


@user_passes_test(admin_only)
def view_order(request, order_id):
    # Fetch the order by its ID, return 404 if not found
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Calculate the total price of the order if needed
    total_price = sum(item.price * item.quantity for item in order.items.all())

    # Pass the order details to the template
    context = {
        'order': order,
        'total_price': total_price,
    }

    return render(request, 'admin_panel/view_order.html', context)



# View to update order status
@user_passes_test(admin_only)
def admin_update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Fetch the order by ID

    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)  # Save but don't commit to the DB yet
            order.updated_at = timezone.now()  # Update the `updated_at` field
            order.save()  # Now save the order

            # Send an email to the user about the order status update
            send_mail(
                subject=f'Order #{order.id} Status Update',
                message=f'Hello {order.user.username},\n\nYour order #{order.id} has been {order.status}.\n\nThank you for shopping with us!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.user.email],
                fail_silently=False,
            )

            # Broadcast the status change to WebSocket clients (users)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'orders_group',  # Broadcast to the group users are connected to
                {
                    'type': 'order_status_update',
                    'order_id': order.id,
                    'order_status': order.status
                }
            )

            messages.success(request, f"Order {order.id} status updated to {order.status}.")
            return redirect('admin_panel:admin_view_order', order_id=order.id)  # Redirect back to order details
    else:
        form = OrderStatusForm(instance=order)

    context = {
        'order': order,
        'form': form,
    }

    return render(request, 'admin_panel/update_order_status.html', context)

@user_passes_test(admin_only)
def admin_manage_users(request):
    return render(request, 'admin_panel/manage_users.html')

@user_passes_test(admin_only)
def admin_settings(request):
    return render(request, 'admin_panel/settings.html')

@user_passes_test(admin_only)
def admin_help(request):
    return render(request, 'admin_panel/help.html')


