# Generated by Django 3.1.7 on 2021-04-30 10:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_auto_20210424_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='saved_by',
            field=models.ManyToManyField(blank=True, related_name='saved_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]