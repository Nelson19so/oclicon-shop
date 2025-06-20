# Generated by Django 5.2 on 2025-06-15 14:21

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_remove_productcomparison_added_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcomparison',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productcomparison',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='product_comparison', to='products.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productcomparison',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='productcomparison',
            unique_together={('session_key', 'product')},
        ),
    ]
