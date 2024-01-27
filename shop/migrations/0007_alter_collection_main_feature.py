# Generated by Django 5.0.1 on 2024-01-26 21:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_product_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='main_feature',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='collections', to='shop.mainfeature', verbose_name='Features'),
        ),
    ]
