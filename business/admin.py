from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'quantity', 'price']
    list_display_link = ['id', 'name']
    list_filter = ["category"]
    search_fields = ['name']
