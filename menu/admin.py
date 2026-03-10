from django.contrib import admin

# Register your models here.
from menu.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    ordering = ('order',)
    list_editable = ('order', 'is_active')


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'food_type', 'is_available')
    list_filter = ('category', 'food_type', 'is_available')
    search_fields = ('name',)