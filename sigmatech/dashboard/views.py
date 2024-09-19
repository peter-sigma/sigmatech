from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


# Create your views here.
@login_required(login_url='signin')
def dashboard(request):
    username = request.user.username
    context = {
        'username': username
    }
    return render(request, 'dashboard/dashboard.html', context)



# Admin restriction
def admin_only(user):
    return user.is_superuser

@user_passes_test(admin_only)
def admin_dashboard(request):
    return render(request, 'dashboard/admindashboard.html')

from django.shortcuts import render, get_object_or_404, redirect
from product.models import Category, Product
from product.forms import CategoryForm, ProductForm
from django.contrib.auth.decorators import user_passes_test

# Check if the user is admin
def admin_only(user):
    return user.is_superuser

# Display all products
@user_passes_test(admin_only)
def admin_manage_products(request):
    products = Product.objects.all()
    return render(request, 'dashboard/manage_products.html', {'products': products})

# Add new product
@user_passes_test(admin_only)
def admin_add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:admin_manage_products')
    else:
        form = ProductForm()
    return render(request, 'dashboard/add_product.html', {'form': form})

# Edit product
@user_passes_test(admin_only)
def admin_edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard:admin_manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/edit_product.html', {'form': form, 'product': product})

# Delete product
@user_passes_test(admin_only)
def admin_delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard:admin_manage_products')
    return render(request, 'dashboard/delete_product.html', {'product': product})

# Manage categories
@user_passes_test(admin_only)
def admin_manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/manage_categories.html', {'categories': categories})

# Add new category
@user_passes_test(admin_only)
def admin_add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:admin_manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/add_category.html', {'form': form})

# View to edit an existing category
@login_required(login_url='signin')
def admin_edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('dashboard:admin_manage_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/edit_category.html', {
        'form': form,
        'category': category
    })

# View to delete a category
@login_required(login_url='signin')
def admin_delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('dashboard:admin_manage_categories')
    return render(request, 'dashboard/delete_category.html', {
        'category': category
    })
    
    
@user_passes_test(admin_only)
def admin_manage_orders(request):
    return render(request, 'dashboard/manage_orders.html')

@user_passes_test(admin_only)
def admin_manage_users(request):
    return render(request, 'dashboard/manage_users.html')

@user_passes_test(admin_only)
def admin_settings(request):
    return render(request, 'dashboard/settings.html')

@user_passes_test(admin_only)
def admin_help(request):
    return render(request, 'dashboard/help.html')
