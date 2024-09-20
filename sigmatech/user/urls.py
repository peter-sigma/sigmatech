from django.contrib import admin
from django.urls import path
from .views import signin, signup, signout, edit_profile, view_profile

app_name = 'user'
urlpatterns = [
    path('signin', signin, name='signin'),
    path('signup', signup, name='signup'),
    path('signout', signout, name='signout'),
    path('editprofile', edit_profile, name='editprofile'),
    path('profile', view_profile, name='profile'),
]