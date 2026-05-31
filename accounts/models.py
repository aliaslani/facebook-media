from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11)
    bio = models.CharField(max_length=1024)
    city = models.CharField(max_length=64)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/avatar.png')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر'

    def __str__(self):
        return self.username
    

class Platform_Choice(models.TextChoices):
    FACEBOOK = 'FB', 'Facebook'
    TWITTER = 'TW', 'Twitter'
    INSTAGRAM = 'IG', 'Instagram'
    LINKEDIN = 'LI', 'LinkedIn'
    GITHUB = 'GH', 'GitHub'
    OTHER = 'OT', 'Other'

class SocialLink(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=2, choices=Platform_Choice.choices)
    url = models.URLField()

    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"





class Contact(models.Model):
    subject = models.CharField(max_length=64)
    sender = models.EmailField()
    message = models.TextField()
    file = models.FileField(upload_to='contacts/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

