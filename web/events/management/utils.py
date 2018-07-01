import re

from datetime import datetime


def get_twitter_handle(data):
    """ Extract twitter handle
    """
    twitter_handle = ""

    if not data:
        return twitter_handle

    # Match patterns like 'https://twitter.com/handle
    regexp = "https:\/\/twitter.com\/(?P<handle>.*)"
    m = re.findall(regexp, data)
    if len(m) > 0:
        twitter_handle = m[0]

    return twitter_handle


def get_date(data):
    """ Parses a date
    """

    # Match patterns like "2019-04-22"
    parsed_date = None
    try:
        parsed_date = datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        pass

    return parsed_date



def get_start_end_dates(data, year=None):
    """ Extract start and end dates for an edition
    """
    event_edition_start = None
    event_edition_end = None

    if not data:
        return event_edition_start, event_edition_end

    # Match patterns like "October 24, 2014"
    regexp = "(?P<month>[a-zA-Z]+)\s(?P<day>[0-9]+),\s(?P<year>[0-9]+)"
    m = re.findall(regexp, data)
    if len(m) > 0:
        month, day, year = m[0]
        date_string = '{:s}/{:s}/{:s}'.format(day, month, year)
        event_edition_start = datetime.strptime(date_string, '%d/%B/%Y')
        event_edition_end = datetime.strptime(date_string, '%d/%B/%Y')

    # Match patterns like "October 24-25, 2014"
    regexp = "(?P<month>[a-zA-Z]+)\s(?P<day_start>[0-9]+)-(?P<day_end>[0-9]+),\s(?P<year>[0-9]+)"
    m = re.findall(regexp, data)
    if len(m) > 0:
        month, day_start, day_end, year = m[0]
        date_string = '{:s}/{:s}/{:s}'.format(day_start, month, year)
        event_edition_start = datetime.strptime(date_string, '%d/%B/%Y')
        date_string = '{:s}/{:s}/{:s}'.format(day_end, month, year)
        event_edition_end = datetime.strptime(date_string, '%d/%B/%Y')

    # Match patterns like "Feb 17–19" and "February 17-19"
    regexp = "(?P<month>[a-zA-Z]+)\s(?P<day_start>[0-9]+)-(?P<day_end>[0-9]+)"
    m = re.findall(regexp, data)
    if len(m) > 0:
        month, day_start, day_end = m[0]
        if month == "Sept":
            month = "September"
        date_string = '{:s}/{:s}/{:s}'.format(day_start, month, year)
        try:
            event_edition_start = datetime.strptime(date_string, '%d/%b/%Y')
        except ValueError:
            event_edition_start = datetime.strptime(date_string, '%d/%B/%Y')
        date_string = '{:s}/{:s}/{:s}'.format(day_end, month, year)
        try:
            event_edition_end = datetime.strptime(date_string, '%d/%b/%Y')
        except ValueError:
            event_edition_end = datetime.strptime(date_string, '%d/%B/%Y')

    return event_edition_start, event_edition_end
