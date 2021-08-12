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


def is_dst(tz, datetime_to_check):
    """Determine whether or not Daylight Savings Time (DST)
    is currently in effect"""

    # Jan 1 of this year, when all tz assumed to not be in dst
    non_dst = datetime.datetime(
        year=datetime.datetime.now().year, month=1, day=1)
    # Make time zone aware based on tz passed in
    non_dst_tz_aware = pytz.timezone(tz).localize(non_dst)

    # if DST is in effect, their offsets will be different
    return not (non_dst_tz_aware.utcoffset() == datetime_to_check.utcoffset())

#################################################
# Test cases
#################################################


# DST in Eastern ends Nov 1, 2020 at 2 am
timezone_eastern = 'US/Eastern'
datetime_dst_eastern = pytz.timezone(timezone_eastern).localize(
    datetime.datetime(year=2020, month=11, day=1))
datetime_non_dst_eastern = pytz.timezone(timezone_eastern).localize(
    datetime.datetime(year=2020, month=11, day=2))
# should print True
print(timezone_eastern, datetime_dst_eastern, "is in dst:",
      is_dst(timezone_eastern, datetime_dst_eastern))
# should print False
print(timezone_eastern, datetime_non_dst_eastern, "is in dst:",
      is_dst(timezone_eastern, datetime_non_dst_eastern))

# DST in Jerusalem ends Oct 25, 2020 at 2 am
timezone_jerusalem = 'Asia/Jerusalem'
datetime_dst_jerusalem = pytz.timezone(timezone_jerusalem).localize(
    datetime.datetime(year=2020, month=10, day=25))
datetime_non_dst_jerusalem = pytz.timezone(timezone_jerusalem).localize(
    datetime.datetime(year=2020, month=10, day=26))
# should print True
print(timezone_jerusalem, datetime_dst_jerusalem, "is in dst:",
      is_dst(timezone_jerusalem, datetime_dst_jerusalem))
# should print False
print(timezone_jerusalem, datetime_non_dst_jerusalem, "is in dst:",
      is_dst(timezone_jerusalem, datetime_non_dst_jerusalem))

# DST in Sydney ends Oct 4, 2020 at 2 am
timezone_sydney = 'Australia/Sydney'
datetime_dst_sydney = pytz.timezone(timezone_sydney).localize(
    datetime.datetime(year=2020, month=10, day=4))
datetime_non_dst_sydney = pytz.timezone(timezone_sydney).localize(
    datetime.datetime(year=2020, month=10, day=5))
# should print True
print(timezone_sydney, datetime_dst_sydney, "is in dst:",
      is_dst(timezone_sydney, datetime_dst_sydney))
# should print False
print(timezone_sydney, datetime_non_dst_sydney, "is in dst:",
      is_dst(timezone_sydney, datetime_non_dst_sydney))

# try with your timezone and current time
timezone_local = 'US/Pacific'
# try with different values of timedelta days; 0 will give current timestamp
datetime_now = pytz.timezone(timezone_local).localize(
    datetime.datetime.now() - datetime.timedelta(days=0))
print(timezone_local, datetime_now, "is in dst:",
      is_dst(timezone_local, datetime_now))
