# Generated by Django 2.0.13 on 2019-04-12 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pandas_csv_app', '0006_auto_20190412_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='columncheck',
            name='max',
        ),
        migrations.RemoveField(
            model_name='columncheck',
            name='min',
        ),
    ]
