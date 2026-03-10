from django.contrib import admin

# Register your models here.
from cart.models import *
admin.site.register(Cart)
admin.site.register(CartItem)