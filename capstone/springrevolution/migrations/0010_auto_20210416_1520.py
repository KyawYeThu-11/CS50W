# Generated by Django 3.1.7 on 2021-04-16 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('springrevolution', '0009_user_receiving_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='receiving_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
