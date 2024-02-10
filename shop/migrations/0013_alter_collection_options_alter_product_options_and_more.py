# Generated by Django 5.0.1 on 2024-02-10 05:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0002_delete_usagecount'),
        ('shop', '0012_homebanner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'verbose_name': 'Collection', 'verbose_name_plural': 'Collections'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AddField(
            model_name='address',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='discount.basediscount', verbose_name='Discount'),
        ),
    ]
