# Generated by Django 5.0.1 on 2024-01-24 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_review_parent_review_alter_cart_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Review', 'verbose_name_plural': 'Reviews'},
        ),
    ]
