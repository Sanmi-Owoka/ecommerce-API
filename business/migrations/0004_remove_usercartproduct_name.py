# Generated by Django 4.1.4 on 2022-12-13 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("business", "0003_usercartproduct_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usercartproduct",
            name="name",
        ),
    ]