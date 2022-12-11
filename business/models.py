from django.db import models
import os
import uuid


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
