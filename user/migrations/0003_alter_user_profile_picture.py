# Generated by Django 5.1.1 on 2024-09-11 10:19

import user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_picture/default_profile.jpg', null=True, upload_to=user.models.rename_profile_picture),
        ),
    ]
