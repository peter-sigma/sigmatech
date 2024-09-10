from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
# Create your views here.
def signin(request):
    return render(request, 'user/signin.html')

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