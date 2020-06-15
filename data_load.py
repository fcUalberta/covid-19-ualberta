"""
Module to preprocess and aggregate quantitative data from input excel sheets
"""
import pandas as pd
import os
import numpy as np

def data_ingest():
    """
    Function to perform Data preprocessing and aggregation of input excel sheets
    to create dataframes in different aggregated versions

    Returns:
    Different versions of dataframes in required format for visualization
    """
    path = r"data1/"
    list = os.listdir(path)
    c=0
    keys = ['Province/State', 'Country/Region', 'Lat', 'Long', 'Date']
    combined_df = pd.read_csv(os.path.join(path,"data.csv"),sep=",")
    combined_df.fillna(0)
    combined_df.rename(columns={'Deaths':'Death'},inplace=True)
    combined_df['Date'] = pd.to_datetime(combined_df['Date']) #Converting to datetype
    for c in ['Lat','Long','Confirmed','Death','Recovered']:
        combined_df[c] = pd.to_numeric(combined_df[c], errors='coerce',downcast='integer')
        combined_df.fillna(0,inplace=True)
        combined_df[c] = combined_df[c].astype(int)
    combined_df.fillna(0,inplace=True) # Filling Nan with 0

    # If no province available, fill with Country/Region
    combined_df['Location'] = np.where(combined_df['Province/State']==0,combined_df['Country/Region'] , combined_df['Province/State'])

    # Adding Active cases field
    combined_df['Active'] = combined_df['Confirmed']-(combined_df['Death']+combined_df['Recovered'])
    combined_df['Active'] = pd.to_numeric(combined_df['Active'], errors='coerce',downcast='integer')
    # Adding Fatality Rate field
    combined_df.loc[combined_df['Death'] == 0, 'Fatality Rate'] = 0
    combined_df.loc[combined_df['Death'] > 0, 'Fatality Rate'] = round((combined_df['Death']/combined_df['Confirmed'])*100,2)
    combined_df.loc[combined_df['Confirmed'] == 0, 'Fatality Rate'] = 0

    combined_df = combined_df.sort_values(['Country/Region','Province/State','Date'], ascending = False)

    # Adding the Daily values for each type of case
    combined_df['New Confirmed'] = combined_df.groupby(['Country/Region','Province/State'])['Confirmed'].diff(periods=-1).fillna(0)
    combined_df['New Death'] = combined_df.groupby(['Country/Region','Province/State'])['Death'].diff(periods=-1).fillna(0)
    combined_df['New Recovered'] = combined_df.groupby(['Country/Region','Province/State'])['Recovered'].diff(periods=-1).fillna(0)
    combined_df = combined_df.sort_values(['Country/Region','Province/State'], ascending = True)

    # Converting the new added fields to integers
    for c in ['New Confirmed','New Death','New Recovered']:
        combined_df[c] = pd.to_numeric(combined_df[c], errors='coerce',downcast='integer')
        combined_df[c] = combined_df[c].astype(int)

    # Writing to a xlsx file for validation during implementation
    combined_df.to_excel(r'combined.xlsx',index=False)

    #  Creating new df after dropping the fields that arent needed
    base_df = combined_df
    # Performing Groupby operation on countries and Date -> Result : Countries with all days
    aggregations = { 'Lat':'first','Long':'first','Confirmed':'sum',
    'Active':'sum','Death':'sum','Recovered':'sum',
    'New Confirmed':'sum','New Death':'sum','New Recovered':'sum'}
    countryDays_df=combined_df.groupby(["Country/Region","Date"],as_index=False).agg(aggregations) #groupby Country and Date values
    countryDays_df.loc[countryDays_df['Death'] == 0, 'Fatality Rate'] = 0
    countryDays_df.loc[countryDays_df['Death'] > 0, 'Fatality Rate'] = round((countryDays_df['Death']/countryDays_df['Confirmed'])*100,2)
    countryDays_df.loc[countryDays_df['Confirmed'] == 0, 'Fatality Rate'] = 0
    countryDays_df['Date'] = pd.to_datetime(countryDays_df['Date']) #Converting to datetype

    # Finding the latest date
    latest_date = combined_df['Date'].max() #Finding latest date

    # Filtering  Countries and provinces with latest date only
    latest_df=base_df.loc[base_df.Date == latest_date].copy()
    latest_df =  latest_df.reset_index(drop=True)
    for c in ['Lat','Long','Confirmed','Death','Active','Recovered','New Confirmed','New Death','New Recovered']:
        latest_df[c] = pd.to_numeric(latest_df[c], errors='coerce',downcast='integer')

    # Creating a copy
    latest_df_copy=latest_df.drop(['Province/State'],axis=1)

    # Performing group by operation on countries alone -> Result: Countries with latest dates
    aggregations = { 'Lat':'first','Long':'first','Confirmed':'sum','Date':'first',
    'Active':'sum','Death':'sum','Recovered':'sum',
    'New Confirmed':'sum','New Death':'sum','New Recovered':'sum'}
    countryLatest_df=latest_df_copy.groupby("Country/Region",as_index=False).agg(aggregations) #groupby Country values
    countryLatest_df.loc[countryLatest_df['Death'] == 0, 'Fatality Rate'] = 0
    countryLatest_df.loc[countryLatest_df['Death'] > 0, 'Fatality Rate'] = round((countryLatest_df['Death']/countryLatest_df['Confirmed'])*100,2)
    countryLatest_df.loc[countryLatest_df['Confirmed'] == 0, 'Fatality Rate'] = 0

    # Creating a dataframe for Canada
    canada_df = latest_df.loc[latest_df['Country/Region'] == 'Canada']
    # Adding population column for province-wise
    canada_pop = {'Province/State': ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador',
        'Northwest Territories', 'Nova Scotia', 'Ontario', 'Prince Edward Island',  'Quebec', 'Saskatchewan', 'Yukon','Nunavut'],
        'Population': [4413146, 5110917, 1377517, 779993, 521365, 44904, 977457, 14711827, 158158, 8537674, 1181666, 41078, 39097]
    }
    canada_pop_df = pd.DataFrame.from_dict(canada_pop)
    canada_df = pd.merge(canada_df,canada_pop_df,how = 'left',on = 'Province/State').fillna(0)
    # Adding a new field for Cases per population
    canada_df.loc[canada_df['Population'] == 0, 'Cases Per Population'] = 0
    canada_df.loc[canada_df['Population'] > 0, 'Cases Per Population'] = round((canada_df['Confirmed']/canada_df['Population'])*100000)
    # Converting the datatype to integer for the newly added fields
    for c in ['Population','Cases Per Population']:
        canada_df[c] = pd.to_numeric(canada_df[c], errors='coerce',downcast='integer')

    # Performing group by operation on Date to get dataframe with sum of global values for all dates
    aggregations = {'Confirmed':'sum','Active':'sum','Death':'sum','Recovered':'sum', 'New Confirmed':'sum','New Death':'sum', 'New Recovered':'sum', 'Fatality Rate':'mean'}
    sum_df=countryDays_df.groupby("Date",as_index=False).agg(aggregations) #groupby Date values

    # print(combined_df,base_df,countryDays_df,latest_df, countryLatest_df.head())
    return base_df,countryDays_df,latest_df, countryLatest_df,canada_df, sum_df
