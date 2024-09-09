from django.shortcuts import render

# Create your views here.
def index(request):
    nav_items = [
        {'name': 'Home', 'url': '/', 'icon': 'fas fa-home'},
        {'name': 'About', 'url': '/about/', 'icon': 'fas fa-info-circle'},
        {'name': 'Windowshop', 'url': '/shop/', 'icon': 'fas fa-shopping-cart'},
        {'name': 'Sign In', 'url': '/signin/', 'icon': 'fas fa-sign-in-alt'},
        {'name': 'Sign Up', 'url': '/signup/', 'icon': 'fas fa-user-plus'}
    ]
    return render(request, 'core/index.html', {'nav_items': nav_items})


def about(request):
    return render(request, 'core/about.html')