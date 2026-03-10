from django.urls import path
from orders.views import *

urlpatterns = [
    path('my_orders/', my_orders, name='my_orders'),
    path('checkout/', checkout, name='checkout'),
]