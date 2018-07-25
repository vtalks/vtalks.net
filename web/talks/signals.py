from django.db.models.signals import post_save

from talks.models import Talk
from talks.events import publish_talk_event


def talk_post_save_callback(sender, instance, **kwargs):
    # Send pipeline.talk event to NATS
    publish_talk_event(instance.youtube_url)

post_save.connect(talk_post_save_callback, sender=Talk)
