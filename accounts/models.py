from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11)
    bio = models.CharField(max_length=1024)
    city = models.CharField(max_length=64)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='avatar.png')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر'

    def __str__(self):
        return self.username