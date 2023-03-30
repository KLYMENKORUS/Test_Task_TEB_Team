from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Model describing the profile"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(blank=True, null=True, upload_to='profile_photo',
                              default='profile_photo/default.jpg')

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'profiles'
