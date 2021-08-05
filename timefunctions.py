#
# @author [Diogo Ribeiro]
# @email [diogo_dj@hotmail.com]
# @create date 2021-08-05 12:59:48
# @modify date 2021-08-05 12:59:48
# @desc datetime functions to calculate days of the week
#
import pytz
import os
import datetime
from dateutil.tz import gettz


def priorSaturday():
    """ calculates the previous saturday from today

    Returns:
        datetime: datetime object 
    """
    return datetime.datetime.now(gettz(os.environ['TZ'])) - datetime.timedelta(days=((datetime.datetime.now(gettz(os.environ['TZ'])).isoweekday() + 1) % 7))


def priorSunday():
    """calculates the previous sunday from today

    Returns:
        datetime: datetime object 
    """
    return priorSaturday() + datetime.timedelta(days=1)


def priorDay(days):
    """calculates the day before or after the previous saturday

    Args:
        days (integer): if positive it goes back days, if it is negative it goes foward days

    Returns:
        datetime: datetime object 
    """
    return priorSaturday() - datetime.timedelta(days=days)


def midnightOffset(offset):
    """[summary]

    Args:
        offset ([type]): [description]

    Returns:
        [type]: [description]
    """

    # Construct a timezone object
    tz = gettz(os.environ['TZ'])

    # Work out today/now as a timezone-aware datetime
    today = datetime.datetime.now(tz)

    # Adjust by the offset. Note that that adding 1 day might actually move us 23 or 25
    # hours into the future, depending on daylight savings. This works because the {today}
    # variable is timezone aware
    target_day = today + datetime.timedelta(days=offset)

    # Discard hours, minutes, seconds and microseconds
    midnight_aware = tz.localize(datetime.datetime.combine(
        target_day, datetime.time(0, 0, 0, 0)), is_dst=True)

    return midnight_aware
