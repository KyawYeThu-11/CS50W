# Generated by Django 3.1.7 on 2021-04-14 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('springrevolution', '0006_auto_20210413_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
