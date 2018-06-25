from django.utils import timezone

from events.models import Event
from events.management import utils


def create_event(event_json_data):
    """ Create an event
    """
    event_name = ""
    if "name" in event_json_data:
        event_name = event_json_data["name"]

    event_twitter_handle = ""
    if "twitter" in event_json_data:
        event_twitter_handle = utils.get_twitter_handle(
            event_json_data['twitter'])

    event_url = ""
    if "url" in event_json_data:
        event_url = event_json_data['url']

    event = Event.objects.create(title=event_name,
                                 twitter=event_twitter_handle,
                                 url=event_url,
                                 created=timezone.now())
    return event


def update_event(event_json_data):
    """ Update an event
    """
    event_name = ""
    if "name" in event_json_data:
        event_name = event_json_data["name"]

    event_twitter_handle = ""
    if "twitter" in event_json_data:
        event_twitter_handle = utils.get_twitter_handle(
            event_json_data['twitter'])

    event_url = ""
    if "url" in event_json_data:
        event_url = event_json_data['url']

    event = Event.objects.get(title=event_name)
    event.title = event_name
    event.twitter = event_twitter_handle
    event.url = event_url

    return event