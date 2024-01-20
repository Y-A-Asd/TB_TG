# Generated by Django 5.0.1 on 2024-01-20 11:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=10, verbose_name='Action')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('table_name', models.CharField(max_length=50, verbose_name='Table Name')),
                ('row_id', models.TextField(blank=True, null=True, verbose_name='Row ID')),
                ('old_value', models.JSONField(null=True, verbose_name='Old Value')),
                ('changes', models.JSONField(null=True, verbose_name='Changes')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Audit Log',
                'verbose_name_plural': 'Audit Logs',
            },
        ),
    ]