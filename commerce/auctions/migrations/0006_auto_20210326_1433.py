# Generated by Django 3.1.7 on 2021-03-26 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210326_1405'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='item_id',
            new_name='item',
        ),
    ]