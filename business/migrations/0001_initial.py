# Generated by Django 4.1.4 on 2022-12-13 11:05

import business.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True, unique=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("groceries", "groceries"),
                            ("accessories", "accessories"),
                            ("laundry_products", "laundry_products"),
                            ("books", "books"),
                            ("stationeries", "stationeries"),
                            ("drinks", "drinks"),
                            ("sea_food", "sea_food"),
                            ("snacks", "snacks"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                ("size", models.CharField(max_length=255, null=True)),
                ("color", models.CharField(max_length=255, null=True)),
                ("quantity", models.IntegerField(blank=True, null=True)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, max_digits=50, null=True),
                ),
                (
                    "cover_image",
                    models.ImageField(
                        null=True, upload_to=business.models.get_avatar_upload_path
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                "ordering": ("-created_at",),
            },
        ),
    ]
