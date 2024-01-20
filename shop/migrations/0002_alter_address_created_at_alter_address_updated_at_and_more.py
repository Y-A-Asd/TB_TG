# Generated by Django 5.0.1 on 2024-01-20 21:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='address',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated at'),
        ),
    ]
