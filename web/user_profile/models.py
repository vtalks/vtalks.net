from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    """User Profile Model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

# Create your signals here.

def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()

signals.post_save.connect(create_or_update_user_profile, sender=User)