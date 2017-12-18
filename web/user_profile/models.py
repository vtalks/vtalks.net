from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    oauth_token = models.CharField('OAuth Token', max_length=100, blank=True)
    oauth_token_secret = models.CharField('OAuth2 Token Secret',
                                          max_length=100, blank=True)
    twitter_id = models.CharField(max_length=100, blank=True)
    avatar = models.URLField('Avatar', blank=True)
    bio = models.TextField('Biography', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
