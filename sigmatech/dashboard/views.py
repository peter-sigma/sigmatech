from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from order.models import Order
from django.shortcuts import render, get_object_or_404, redirect
from product.models import Category, Product
from product.forms import CategoryForm, ProductForm
from .forms import OrderStatusForm
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
@login_required(login_url='user:signin')
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



# Check if the user is admin
def admin_only(user):
    return user.is_superuser

