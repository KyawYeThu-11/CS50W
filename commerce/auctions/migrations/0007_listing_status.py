# Generated by Django 3.1.7 on 2021-03-26 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210326_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='status',
            field=models.CharField(default='active', max_length=16),
        ),
    ]