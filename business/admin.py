from django.contrib import admin
from .models import Product, UserCartProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'quantity', 'price']
    list_display_link = ['id', 'name']
    list_filter = ["category"]
    search_fields = ['name']

@admin.register(UserCartProduct)
class UserCartProduct(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity', 'total_amount', 'created_at', 'updated_at']
    list_display_link = ['id', 'product']
    search_fields = ['product__name']
