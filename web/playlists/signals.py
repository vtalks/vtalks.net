from django.db.models.signals import post_save

from playlists.models import Playlist
from playlists.events import publish_playlist_event


def playlist_post_save_callback(sender, instance, **kwargs):
    # Send pipeline.playlist event to NATS
    publish_playlist_event(instance.youtube_url)


post_save.connect(playlist_post_save_callback, sender=Playlist)
