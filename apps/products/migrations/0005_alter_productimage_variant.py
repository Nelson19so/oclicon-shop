# Generated by Django 5.2 on 2025-05-26 15:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_productimage_variant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product'),
        ),
    ]
