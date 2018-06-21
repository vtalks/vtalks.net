import re

from datetime import timedelta


def parse_duration(duration_string):
    hours = 0
    minutes = 0
    seconds = 0
    duration = duration_string
    try:
        hours = re.compile('(\d+)H').search(duration).group(1)
    except AttributeError:
        hours = 0
    try:
        minutes = re.compile('(\d+)M').search(duration).group(1)
    except AttributeError:
        minutes = 0
    try:
        seconds = re.compile('(\d+)S').search(duration).group(1)
    except AttributeError:
        seconds = 0
    d = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    return d