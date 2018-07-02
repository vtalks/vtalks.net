from django.utils import timezone

from events.models import Edition
from events.management import utils


def create_event_edition(event_json_data, year, event):
    """ Create an event edition
    """
    event_edition_name = ""
    if "name" in event_json_data:
        event_edition_name = "{:s} {:s}".format(event_json_data["name"], year)

    event_edition_url = ""
    if "url" in event_json_data:
        event_edition_url = event_json_data['url']

    event_edition_country = ""
    if "country" in event_json_data:
        event_edition_country = event_json_data['country']

    event_edition_city = ""
    if "city" in event_json_data:
        event_edition_city = event_json_data['city']

    event_edition_start = ""
    event_edition_end = ""
    if "date" in event_json_data:
        event_edition_start, event_edition_end = utils.get_start_end_dates(event_json_data['date'])

    if "startDate" in event_json_data:
        event_edition_start = utils.get_date(event_json_data['startDate'])

    if "endDate" in event_json_data:
        event_edition_end = utils.get_date(event_json_data['endDate'])

    event_edition = Edition.objects.create(title=event_edition_name,
                                           url=event_edition_url,
                                           country=event_edition_country,
                                           city=event_edition_city,
                                           event=event,
                                           event_start=event_edition_start,
                                           event_end=event_edition_end,
                                           created=timezone.now())
    return event_edition


def update_event_edition(event_json_data, year, event):
    """ Update an event edition
    """
    event_edition_name = ""
    if "name" in event_json_data:
        event_edition_name = "{:s} {:s}".format(event_json_data["name"], year)

    event_edition_url = ""
    if "url" in event_json_data:
        event_edition_url = event_json_data['url']

    event_edition_country = ""
    if "country" in event_json_data:
        event_edition_country = event_json_data['country']

    event_edition_city = ""
    if "city" in event_json_data:
        event_edition_city = event_json_data['city']

    event_edition_start = None
    event_edition_end = None
    if "date" in event_json_data:
        event_edition_start, event_edition_end = utils.get_start_end_dates(event_json_data['date'], year)

    if "startDate" in event_json_data:
        event_edition_start = utils.get_date(event_json_data['startDate'])

    if "endDate" in event_json_data:
        event_edition_end = utils.get_date(event_json_data['endDate'])

    event_edition = Edition.objects.get(title=event_edition_name)
    event_edition.title = event_edition_name
    event_edition.url = event_edition_url
    event_edition.country = event_edition_country
    event_edition.city = event_edition_city
    event_edition.event = event
    if event_edition_start:
        event_edition.event_start = event_edition_start
    if event_edition_end:
        event_edition.event_end = event_edition_end

    return event_edition
