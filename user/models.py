from django.db import models
from django.contrib.auth.models import AbstractUser

import os
import datetime

def rename_profile_picture(instance, filename):
    name, ext = os.path.splitext(filename)
    new_name = instance.username.lower() + datetime.datetime.now().strftime('-%Y-%b-%d-%H-%M-%S') + ext
    print(new_name)
    return '{}/{}'.format('profile_picture', new_name)

class User(AbstractUser):
    bio = models.TextField(max_length=500, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=rename_profile_picture, default='profile_picture/default_profile.jpg', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.username}"