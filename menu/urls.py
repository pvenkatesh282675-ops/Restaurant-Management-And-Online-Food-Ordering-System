from django.urls import path
from menu.views import *
urlpatterns = [
    path('menu', menu, name="menu"),
]