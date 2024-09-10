# user/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    address = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Type in your address'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'address']
        
        

class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Type in your username',
            'id': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Type in your password',
            'id': 'password'
        })
    )