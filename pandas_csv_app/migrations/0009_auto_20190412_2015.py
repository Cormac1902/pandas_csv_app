# Generated by Django 2.0.13 on 2019-04-12 19:15

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pandas_csv_app', '0008_auto_20190412_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='columncheck',
            name='allowed_values',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default={}, size=None),
        ),
    ]
