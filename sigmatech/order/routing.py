from django.urls import re_path
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/orders/$', consumers.OrderConsumer.as_asgi()),
    path('ws/hello/', consumers.HelloWorldConsumer.as_asgi()),
]