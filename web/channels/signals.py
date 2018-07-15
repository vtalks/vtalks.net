from django.db.models.signals import post_save

from channels.models import Channel
from channels.events import publish_channel_event


def channel_post_save_callback(sender, instance, **kwargs):
    # Send pipeline.channel event to NATS
    publish_channel_event(instance.youtube_url)


post_save.connect(channel_post_save_callback, sender=Channel)
