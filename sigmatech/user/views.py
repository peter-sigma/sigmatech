from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, SignInForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
# Create your views here.
def signin(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')  # Replace 'home' with your homepage's URL name
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = SignInForm()
    
    return render(request, 'user/signin.html', {'form': form})

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Adjust this to your desired redirect page
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/signup.html', {'form': form})