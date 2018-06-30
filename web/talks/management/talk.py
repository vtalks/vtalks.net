from datetime import datetime

from django.core import management
from django.utils import timezone

from channels.models import Channel
from playlists.models import Playlist
from talks.models import Talk
from talks.utils import parse_duration

from youtube_data_api3.channel import get_channel_youtube_url


def recalculate_talk_sortrank(talk):
    """ Recalculates sort and ranking values given model's statistics
    """
    # wilson score
    wilsonscore_rank = talk.get_wilson_score(talk.total_like_count, talk.total_dislike_count)
    talk.wilsonscore_rank = wilsonscore_rank

    # hacker news hot
    votes = abs(talk.total_like_count - talk.total_dislike_count)
    hacker_hot = talk.get_hacker_hot(votes, talk.created)
    talk.hacker_hot = hacker_hot

    return talk


def update_talk_statistics(talk, talk_json_data):
    """ Updates youtube video statistics ( likes, dislikes, favorites and
    views )
    """
    if "statistics" in talk_json_data:
        statistics = talk_json_data["statistics"]
        if "viewCount" in statistics:
            talk.youtube_view_count = statistics["viewCount"]
        if "likeCount" in statistics:
            talk.youtube_like_count = statistics["likeCount"]
        if "dislikeCount" in statistics:
            talk.youtube_dislike_count = statistics["dislikeCount"]
        if "favoriteCount" in statistics:
            talk.youtube_favorite_count = statistics["favoriteCount"]

    return talk


def update_talk_tags(talk, talk_json_data):
    """ Updates tags associated to this model instance
    """
    tags = []
    if "snippet" in talk_json_data:
        snippet = talk_json_data["snippet"]
        if "tags" in snippet:
            tags += snippet["tags"]
    for tag in tags:
        talk.tags.add(tag)

    return talk


def update_talk_model(talk, talk_json_data):
    """ Updates model's common properties
    """
    talk.code = talk_json_data["id"]
    if "snippet" in talk_json_data:
        snippet = talk_json_data["snippet"]
        if "title" in snippet:
            talk.title = talk_json_data["snippet"]["title"]
        if "description" in snippet:
            talk.description = talk_json_data["snippet"]["description"]
        if "publishedAt" in snippet:
            published_at = talk_json_data["snippet"]["publishedAt"]
            datetime_published_at = datetime.strptime(published_at,"%Y-%m-%dT%H:%M:%S.000Z")
            datetime_published_at = datetime_published_at.replace(tzinfo=timezone.utc)
            talk.created = datetime_published_at
    if "contentDetails" in talk_json_data:
        content_details = talk_json_data["contentDetails"]
        if "duration" in content_details:
            talk.duration = parse_duration(content_details["duration"])

    return talk


def create_talk(talk_json_data, playlist=None):
    """ Create a new Talk into the database
    """
    talk_code = talk_json_data["id"]
    if "snippet" in talk_json_data:
        snippet = talk_json_data["snippet"]
        if "title" in snippet:
            talk_title = talk_json_data["snippet"]["title"]
        if "description" in snippet:
            talk_description = talk_json_data["snippet"]["description"]
        if "publishedAt" in snippet:
            published_at = talk_json_data["snippet"]["publishedAt"]
            datetime_published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S.000Z")
            datetime_published_at = datetime_published_at.replace(tzinfo=timezone.utc)
            talk_created = datetime_published_at
        if "channelId" in snippet:
            channel_code = talk_json_data["snippet"]["channelId"]
            youtube_url_channel = get_channel_youtube_url(channel_code)
            management.call_command("update_channel", youtube_url_channel)
            talk_channel = Channel.objects.get(code=channel_code)
        if "contentDetails" in talk_json_data:
            content_details = talk_json_data["contentDetails"]
            if "duration" in content_details:
                talk_duration = parse_duration(content_details["duration"])

    talk = Talk.objects.create(
        code=talk_code,
        title=talk_title,
        description=talk_description,
        duration=talk_duration,
        channel=talk_channel,
        created=talk_created,
        updated=timezone.now(),
    )
    talk = update_talk_tags(talk, talk_json_data)
    talk = update_talk_statistics(talk, talk_json_data)
    talk = recalculate_talk_sortrank(talk)

    if playlist:
        talk.playlist = Playlist.objects.get(code=playlist)

    talk.save()

    return talk


def update_talk(talk, talk_json_data, playlist=None):
    """ Update an existing Talk into the database
    """
    talk.code = talk_json_data["id"]

    talk = update_talk_model(talk, talk_json_data)
    talk = update_talk_tags(talk, talk_json_data)
    talk = update_talk_statistics(talk, talk_json_data)
    talk = recalculate_talk_sortrank(talk)

    if "snippet" in talk_json_data:
        snippet = talk_json_data["snippet"]
        if "channelId" in snippet:
            channel_code = talk_json_data["snippet"]["channelId"]
            youtube_url_channel = get_channel_youtube_url(channel_code)
            management.call_command("update_channel", youtube_url_channel)
            talk.channel = Channel.objects.get(code=channel_code)

    if playlist:
        talk.playlist = Playlist.objects.get(code=playlist)

    talk.save()

    return talk
