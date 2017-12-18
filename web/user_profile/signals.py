from django.db.models import signals
from django.contrib.auth.models import User

from .models import UserProfile

# Create your signals here.


def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


signals.post_save.connect(create_or_update_user_profile, sender=User)
