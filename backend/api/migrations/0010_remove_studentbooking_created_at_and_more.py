# Generated by Django 5.1.7 on 2025-04-24 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_userauth_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentbooking',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='studentbooking',
            name='confirmed',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
