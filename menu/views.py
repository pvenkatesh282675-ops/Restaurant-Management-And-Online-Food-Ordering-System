from django.shortcuts import render

# Create your views here.

from menu.models import Category

def menu(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, "menu.html", {"categories": categories})