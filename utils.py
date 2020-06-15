"""
Module for additional utility files used in the application
"""
import datetime

# Getting the timestamp in UTC format
epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    """
    Function to return the seconds difference between two dates

    Args:
    dt: Source date
    
    Returns: The timestamp difference
    """
    return (dt - epoch).total_seconds()

def get_marks_from_start_end(start, end):
    '''
    Function to convert the difference in time to a date format

    Args:
    start : Starting timestamp
    end: Ending timestamp

    Returns:
    A dict with one item per month
    {1440080188.1900003: '2015-08',
    '''
    result = []
    current = start
    while current <= end:
        result.append(current)
        current += relativedelta(months=1)
    return {unix_time_millis(m):(str(m.strftime('"%m/%d/%Y'))) for m in result}

def create_divs(case):

    """
    Function to return a list of Div tags with Country name and value of 'case' column

    Args:
    case: The column selected by the Dropdown

    Returns: A lsit of div tags with country name and the value of 'case' column
    """

    return_divs = []
    for country in countries:
        newdf = country_df.loc[country_df['Country/Region'] == country]
        return_divs.append(html.Div(html.P(country+" "+newdf[case].astype(int).apply(str), style = {'font-size': '10px'})))
    return return_divs
