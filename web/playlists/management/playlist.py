from datetime import datetime

from django.utils import timezone

from playlists.models import Playlist


def create_playlist(playlist_json_data):
    """ Create a new Playlist into the database
    """
    playlist_code = playlist_json_data["id"]
    if "snippet" in playlist_json_data:
        snippet = playlist_json_data["snippet"]
        if "title" in snippet:
            playlist_title = playlist_json_data["snippet"]["title"]
        if "description" in snippet:
            playlist_description = playlist_json_data["snippet"]["description"]
        if "publishedAt" in snippet:
            published_at = playlist_json_data["snippet"]["publishedAt"]
            datetime_published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S.000Z")
            datetime_published_at = datetime_published_at.replace(tzinfo=timezone.utc)
            playlist_created = datetime_published_at

    playlist = Playlist.objects.create(code=playlist_code,
                                       title=playlist_title,
                                       description=playlist_description,
                                       created=playlist_created)

    return playlist


def update_playlist(playlist, playlist_json_data):
    """ Updates an existing Playlist into the database
    """
    playlist.code = playlist_json_data["id"]
    if "snippet" in playlist_json_data:
        snippet = playlist_json_data["snippet"]
        if "title" in snippet:
            playlist.title = playlist_json_data["snippet"]["title"]
        if "description" in snippet:
            playlist.description = playlist_json_data["snippet"]["description"]
        if "publishedAt" in snippet:
            published_at = playlist_json_data["snippet"]["publishedAt"]
            datetime_published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S.000Z")
            datetime_published_at = datetime_published_at.replace(tzinfo=timezone.utc)
            playlist.created = datetime_published_at

    playlist.save()

    return playlist