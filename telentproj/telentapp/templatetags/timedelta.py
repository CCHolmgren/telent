from math import floor
from django import template

register = template.Library()


@register.filter
def timedelta(value, time_format="{days} days, {hours2}:{minutes2}:{seconds2}"):
    import datetime
    from django.utils.timezone import utc

    if isinstance(value, datetime.datetime):
        value = datetime.datetime.utcnow().replace(tzinfo=utc) - value

    if hasattr(value, 'seconds'):
        seconds = value.seconds + value.days * 24 * 3600
    else:
        seconds = int(value)

    seconds_total = seconds

    minutes = int(floor(seconds / 60))
    minutes_total = minutes
    seconds -= minutes * 60

    hours = int(floor(minutes / 60))
    hours_total = hours
    minutes -= hours * 60

    days = int(floor(hours / 24))
    days_total = days
    hours -= days * 24

    weeks = int(floor(days/7))
    days_without_weeks = days - (weeks * 7)

    years = int(floor(days / 365))
    years_total = years
    days -= years * 365

    return time_format.format(**{
        'seconds': seconds,
        'seconds2': str(seconds).zfill(2),
        'minutes': minutes,
        'minutes2': str(minutes).zfill(2),
        'hours': hours,
        'hours2': str(hours).zfill(2),
        'days': days,
        'years': years,
        'weeks': weeks,
        'days_without_weeks': days_without_weeks,
        'seconds_total': seconds_total,
        'minutes_total': minutes_total,
        'hours_total': hours_total,
        'days_total': days_total,
        'years_total': years_total,
    })
