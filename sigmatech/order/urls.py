from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'order'
urlpatterns = [
    path('hello/', hello_world_view, name='hello_world'),
    path('order/', order_list, name='order'),
]