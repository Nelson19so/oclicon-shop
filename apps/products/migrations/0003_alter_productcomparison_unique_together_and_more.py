# Generated by Django 5.2 on 2025-06-15 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_searchhistory_productcomparison_productrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcomparison',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='productcomparison',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.RemoveField(
            model_name='productcomparison',
            name='session_id',
        ),
    ]
