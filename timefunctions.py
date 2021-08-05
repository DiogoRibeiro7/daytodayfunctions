#
# @author [Diogo Ribeiro]
# @email [diogo_dj@hotmail.com]
# @create date 2021-08-05 12:59:48
# @modify date 2021-08-05 12:59:48
# @desc datetime functions to calculate days of the week
#
import datetime

def priorSaturday():
    """ calculates the previous saturday from today

    Returns:
        datetime: datetime object 
    """
    return datetime.datetime.now() - datetime.timedelta(days=((datetime.datetime.now().isoweekday() + 1) % 7))

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

