from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, SignInForm,ProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import UserProfile


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
                
                # Get the 'next' parameter from the URL if present
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('dashboard:dashboard')  # Fallback if 'next' is not provided
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = SignInForm()

    return render(request, 'user/signin.html', {'form': form})

    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard:dashboard')  
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
            return redirect('core:index') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/signup.html', {'form': form})


@login_required(login_url='user:signin')
def signout(request):
    logout(request)
    return redirect('user:signup')
 

@login_required
def view_profile(request):
    return render(request, "user/profile.html")
    
    
    
    
@login_required(login_url='user:signin')
def edit_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)
        user_profile.save()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user:profile')  # Redirect to the profile page or a success page
    else:
        form = ProfileForm(instance=user_profile)
    form = "form"
    return render(request, 'user/editprofile.html', {'form': form})
