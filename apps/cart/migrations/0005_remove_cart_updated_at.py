# Generated by Django 5.2 on 2025-05-30 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_wishlistproduct_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='updated_at',
        ),
    ]
