from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test


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

@user_passes_test(admin_only)
def admin_manage_products(request):
    return render(request, 'dashboard/manage_products.html')

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
