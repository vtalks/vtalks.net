from django.db.models.signals import post_save

from talks.models import Talk
from talks.events import publish_talk_event
from playlists.events import publish_playlist_event


def talk_post_save_callback(sender, instance, **kwargs):
    # Send pipeline.talk event to NATS
    publish_talk_event(instance.youtube_url)

    # Send pipeline.playlist event to NATS (as playlistId is not returned by Youtube)
    if instance.playlist:
        publish_playlist_event(instance.playlist.youtube_url)


post_save.connect(talk_post_save_callback, sender=Talk)
