from django.db import models
import os
import uuid
from users.models import User


def get_avatar_upload_path(instance, filename):
    return os.path.join("product/image/{}/{}".format(instance.name, filename))


class Product(models.Model):
    CATEGORY_CHOICES = (
        ("groceries", "groceries"),
        ("accessories", "accessories"),
        ("laundry_products", "laundry_products"),
        ("books", "books"),
        ("stationeries", "stationeries"),
        ("drinks", "drinks"),
        ("sea_food", "sea_food"),
        ("snacks", "snacks"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, unique=True)
    category = models.CharField(max_length=255, null=True, choices=CATEGORY_CHOICES)
    size = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=255, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=50, null=True, decimal_places=2)
    cover_image = models.ImageField(null=True, upload_to=get_avatar_upload_path)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ("-created_at",)


class UserCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="users_cart")
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class UserCartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="users_cart_product")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="users_items")
    quantity = models.IntegerField(null=True)
    total_amount = models.DecimalField(max_digits=50, null=True, decimal_places=2)
    cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, null=True, related_name="product_cart")
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
