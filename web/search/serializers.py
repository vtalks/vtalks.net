import datetime
from datetime import datetime

from django.utils import timezone


def serialize_json(talk):
    """ Serializes a Talk to JSON
    """
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)

    talk_dict = {
        "id": talk.id,
        "title": talk.title,
        "description": talk.description,
        "view_count": talk.view_count,
        "like_count": talk.like_count,
        "dislike_count": talk.dislike_count,
        "favorite_count": talk.favorite_count,
        "youtube_view_count": talk.youtube_view_count,
        "youtube_like_count": talk.youtube_like_count,
        "youtube_dislike_count": talk.youtube_dislike_count,
        "youtube_favorite_count": talk.youtube_favorite_count,
        "wilsonscore_rank": talk.wilsonscore_rank,
        "hacker_hot": talk.hacker_hot,
        "tags": [],
        "created": (talk.created - epoch).total_seconds() * 1000.0
    }

    if talk.channel:
        talk_dict["channel"] = {
            "id": talk.channel.id,
            "title": talk.channel.title,
            "description": talk.channel.description
        }

    if talk.playlist:
        talk_dict["playlist"] = {
            "id": talk.playlist.id,
            "title": talk.playlist.title,
            "description": talk.playlist.description
        }

    for tag in talk.tags.all():
        talk_dict["tags"].append(tag.name)

    talk_json = talk_dict

    return talk_json

