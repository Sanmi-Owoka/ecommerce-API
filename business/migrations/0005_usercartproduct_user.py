# Generated by Django 4.1.4 on 2022-12-13 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("business", "0004_remove_usercartproduct_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="usercartproduct",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="users_cart_product",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
