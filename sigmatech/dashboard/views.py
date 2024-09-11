from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Create your views here.
@login_required(login_url='signin')
def dashboard(request):
    username = request.user.username
    context = {
        'username': username
    }
    return render(request, 'dashboard/dashboard.html', context)