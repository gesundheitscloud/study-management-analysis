import pandas as pd
from datetime import date
import math
import matplotlib.pyplot as plt

def get_age_group(year_of_birth):
    if pd.isnull(year_of_birth) | year_of_birth == 0: 
        return 'None'
    year_now = date.today().year
    age = year_now - year_of_birth
    dec_year = 10 * math.floor(age/10)
    if dec_year >= 60:
        return ">60"
    return f'{dec_year}-{10+dec_year}'

def to_week_number(day):    
    week_now = day.date().isocalendar()[1]
    year_now = day.date().isocalendar()[0]
    return f'{year_now}, {week_now}'

def plot_over_weeks(df, date_column, ax, title, ylabel, xlabel):
    result = df.loc[~pd.isnull(df[date_column])][['ALP_ID', date_column]].copy()
    result['week'] = result[date_column].apply(lambda x: to_week_number(x))
    week_groups = result.groupby(by=['week'])['ALP_ID'].count()
    week_groups.plot(kind='bar',legend=None, title=title, ax=ax, ylabel=ylabel, xlabel=xlabel);

