from datetime import datetime

from django.utils import timezone

from channels.models import Channel


def create_channel(channel_json_data):
    """ Create a new Channel into the database
    """
    channel_code = channel_json_data["id"]
    if "snippet" in channel_json_data:
        snippet = channel_json_data["snippet"]
        if "title" in snippet:
            channel_title = channel_json_data["snippet"]["title"]
        if "description" in snippet:
            channel_description = channel_json_data["snippet"]["description"]
        if "publishedAt" in snippet:
            published_at = channel_json_data["snippet"]["publishedAt"]
            datetime_published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S.000Z")
            datetime_published_at = datetime_published_at.replace(tzinfo=timezone.utc)
            channel_created = datetime_published_at

    channel = Channel.objects.create(code=channel_code,
                                     title=channel_title,
                                     description=channel_description,
                                     created=channel_created)

    return channel


def update_channel(channel, channel_json_data):
    """ Updates an existing Channel into the database
    """
    channel.code = channel_json_data["id"]
    if "snippet" in channel_json_data:
        snippet = channel_json_data["snippet"]
        if "title" in snippet:
            channel.title = channel_json_data["snippet"]["title"]
        if "description" in snippet:
            channel.description = channel_json_data["snippet"]["description"]
        if "publishedAt" in snippet:
            published_at = channel_json_data["snippet"]["publishedAt"]
            datetime_published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S.000Z")
            datetime_published_at = datetime_published_at.replace(tzinfo=timezone.utc)
            channel.created = datetime_published_at

    channel.save()

    return channel
