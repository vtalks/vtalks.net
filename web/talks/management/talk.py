from datetime import datetime

from django.core import management
from django.utils import timezone

from channels.models import Channel
from talks.models import Talk
from talks.utils import parse_duration

from youtube_data_api3.channel import get_channel_youtube_url


def create_talk(talk_json_data):
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
    talk.update_video_tags(talk_json_data)
    talk.update_video_statistics(talk_json_data)
    talk.recalculate_video_sortrank()

    talk.save()

    return talk


def update_talk(talk, talk_json_data):
    """ Update an existing Talk into the database
    """
    talk.code = talk_json_data["id"]

    talk.update_video_model(talk_json_data)
    talk.update_video_tags(talk_json_data)
    talk.update_video_statistics(talk_json_data)
    talk.recalculate_video_sortrank()

    if "snippet" in talk_json_data:
        snippet = talk_json_data["snippet"]
        if "channelId" in snippet:
            channel_code = talk_json_data["snippet"]["channelId"]
            youtube_url_channel = get_channel_youtube_url(channel_code)
            management.call_command("update_channel", youtube_url_channel)
            talk.channel = Channel.objects.get(code=channel_code)

    talk.save()

    return talk
