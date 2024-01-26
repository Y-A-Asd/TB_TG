# Generated by Django 5.0.1 on 2024-01-26 04:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_remove_review_name_review_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='shop.customer', verbose_name='Customer'),
            preserve_default=False,
        ),
    ]
