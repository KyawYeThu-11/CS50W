# Generated by Django 3.1.7 on 2021-04-24 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='_user_followers_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='love',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
