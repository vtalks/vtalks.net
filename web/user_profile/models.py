from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    oauth_token = models.CharField('OAuth Token', max_length=100, blank=True)
    oauth_token_secret = models.CharField('OAuth2 Token Secret', max_length=100, blank=True)
    twitter_id = models.CharField('Twitter ID', max_length=100, blank=True)
    avatar = models.URLField('Avatar', blank=True)
    bio = models.TextField('Biography', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        get_latest_by = ["-user__date_joined"]
        ordering = ['-user__date_joined']


def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


signals.post_save.connect(create_or_update_user_profile, sender=User)
