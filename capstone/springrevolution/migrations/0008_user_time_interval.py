# Generated by Django 3.1.7 on 2021-04-15 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('springrevolution', '0007_auto_20210414_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='time_interval',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]