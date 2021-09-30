import pandas as pd
import numpy as np
from mysense.utils import ewma
import pytest 
from pandas.testing import assert_frame_equal

PERIOD = 12  # hours to discount to shift the toilet use from the night period to the previous day
SPANS = [7]
PERIODS = ['day', 'night']
night_time = 9
day_time = 21

def load_data_1():
    df = pd.DataFrame()
    return df

def load_data_2():
    df = pd.DataFrame([[2,3]],
                      columns =['day','night'])
    return df

def load_data_3():
    df = pd.DataFrame([[2,3],
                      [0,1]],
                      columns =['day','night'])
    return df

def get_regular_avg(new_value, current_average, sd, span):
    """

    :param new_value:
    :param current_average:
    :param sd:
    :return:
    """
    if current_average == 0:
        return new_value, 0
    else:
        returned = ewma(new_value, current_average, sd, span)
        return returned[0], returned[1]

def day_key_to_update_avg(x,period):
    if period == 'day':
        return f"{x}DayAverageDay"
    else:
        return f"{x}DayAverageNight"

def day_key_to_update_std(x,period):
    if period == 'day':
        return f"{x}DayStdDay"
    else:
        return f"{x}DayStdNight"

def update_stats(x,period):
    if period == 'day':
        return f"{x}DayAverage"
    else:
        return f"{x}NightAverage"

def update_u_info_avg(x,period):
    if period == 'day':
        return f"{x}DayAverage"
    else:
        return f"{x}NightAverage"

def update_u_info_std(x,period):
    if period == 'day':
        return f"{x}DayStd"
    else:
        return f"{x}NightStd"


def toiletMovingAverage(df):
    
    if df is None:
        return pd.DataFrame()
    if df.empty: # get out of the fucntion, the user does't have data
        return df

    for period in PERIODS:
        for span in SPANS:
            current_avg = 0
            current_std = 0
            df[day_key_to_update_avg(span,period)] = 0
            df[day_key_to_update_std(span,period)] = 0
            for row in df.itertuples():
                value_toilet = df.loc[row[0], period]
                current_avg,current_std = get_regular_avg(value_toilet,current_avg,current_std,span) #apply the function ewma
                df.loc[row[0],day_key_to_update_avg(span,period)] = np.round(current_avg,2) # create the avg column
                df.loc[row[0],day_key_to_update_std(span,period)] = np.round(current_std,2) # create the std column

    return df






def test_toiletMovingAverage_1():   
    data = load_data_1()
    expected = pd.DataFrame()
    assert_frame_equal(expected.reset_index(drop=True),toiletMovingAverage(data).reset_index(drop=True))

def test_toiletMovingAverage_2():
    data = None
    expected = pd.DataFrame()
    assert_frame_equal(expected.reset_index(drop=True),toiletMovingAverage(data).reset_index(drop=True))

def test_toiletMovingAverage_3():
    data = load_data_2()
    expected = pd.DataFrame([[2,3,2,0,3,0]],
                      columns =['day','night','7DayAverageDay','7DayStdDay','7DayAverageNight','7DayStdNight'])
    assert_frame_equal(expected.reset_index(drop=True),toiletMovingAverage(data).reset_index(drop=True))

def test_toiletMovingAverage_4():
    data = load_data_3()
    expected = pd.DataFrame([[2,3,2,0,3,0],
                             [0,1,1.5,0.87,2.5,0.87]],
                      columns =['day','night','7DayAverageDay','7DayStdDay','7DayAverageNight','7DayStdNight'])
    assert_frame_equal(expected.reset_index(drop=True),toiletMovingAverage(data).reset_index(drop=True))

