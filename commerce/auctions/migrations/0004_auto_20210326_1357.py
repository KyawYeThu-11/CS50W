# Generated by Django 3.1.7 on 2021-03-26 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210326_1353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='item_id',
            new_name='item',
        ),
    ]
