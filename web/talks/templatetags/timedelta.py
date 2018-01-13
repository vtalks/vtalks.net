from django import template

register = template.Library()


def timedelta_nozeros(value):
    if not value:
        return ''
    minutes, seconds = divmod(value.seconds + value.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    res = "{:02}".format(seconds)
    if minutes > 0:
        res = "{:02}:{}".format(minutes, res)
    if hours > 0:
        res = "{:02}:{}".format(hours, res)
    return res


register.filter('timedelta_nozeros', timedelta_nozeros)
