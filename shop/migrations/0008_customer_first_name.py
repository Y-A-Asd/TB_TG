# Generated by Django 5.0.1 on 2024-01-26 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_cart_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='first_name',
            field=models.CharField(default=1, max_length=255, verbose_name='First Name'),
            preserve_default=False,
        ),
    ]
