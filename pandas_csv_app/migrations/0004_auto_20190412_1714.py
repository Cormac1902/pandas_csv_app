# Generated by Django 2.0.13 on 2019-04-12 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pandas_csv_app', '0003_auto_20190412_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='columncheck',
            name='null_values',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='columncheck',
            name='special_characters',
            field=models.BooleanField(default=False),
        ),
    ]