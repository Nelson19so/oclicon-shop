# Generated by Django 5.2 on 2025-05-26 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_badge_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productspecification',
            name='memory',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='productspecification',
            name='size',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='productspecification',
            name='storage',
            field=models.CharField(),
        ),
    ]
