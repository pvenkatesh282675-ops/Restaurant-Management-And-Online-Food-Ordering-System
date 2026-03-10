from django.urls import path
from cart.views import *

urlpatterns = [
    path('view_cart/', view_cart, name='view_cart'),
    path('add/<int:food_id>/', add_to_cart, name='add_to_cart'),
    path('decrease/<int:item_id>/',decrease_quantity, name='decrease_quantity'),
    path('remove/<int:item_id>/', remove_item, name='remove_item'),
]