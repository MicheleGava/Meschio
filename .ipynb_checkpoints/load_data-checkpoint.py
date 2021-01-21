### required libraries
# data wrangling
import pandas as pd 
import numpy as np
# scraping
from bs4 import BeautifulSoup 
import requests as rq

def levels_to_df(years_list, stations_list, verbose=False):
    '''
    for every year and station, retrieves levels
    than stores all data in a single pandas dataframe and returns
    '''
    
    complete = []

    for year in years_list:
        for station in stations_list:
            if verbose:
                print('Year: ' + year + ' \t ' + 'Station: ' + station)
            complete.append(retrieve_level(year, station))
    
    if verbose:
        print('preparing dataframe...')
    return to_dataframe(complete)


def retrieve_level(year, station):
    '''
    Download csv file for the year and station specified in parameters
    Returns: list in wide format: station_id, year, type, Jan, Feb, ecc.
    '''
    
    BASE_URL = 'https://www.arpa.veneto.it/bollettini/storico/'
    PAGE_SFX = '_LIVIDRO.htm'
    
    url = BASE_URL+year+'/'+station+'_'+year+PAGE_SFX
    
    soup = BeautifulSoup(rq.get(url).content, features='lxml')
    tables_list = soup.find_all("table")
    rows = [] ##list of rows to return

    
    for n, table in enumerate([tables_list[2], tables_list[5], tables_list[8]]):
        #table2: min level, table5: avg level, table8: max level (daily data)
        if n == 0:
            lev_type = 'MIN'
        elif n == 1:
            lev_type = 'AVG'
        else:
            lev_type = 'MAX'
    
   
        for tr in table.find_all('tr')[1:32]:
            row = []
            row.append(year)
            row.append(station)
            row.append(lev_type)
    
            for j, elem in enumerate(tr.find_all()): 
                if j == 0 and elem.name == 'th':
                    row.append(elem.text)
                else:    
                    if elem.name == 'td':
                        if elem.text == '>>':
                            row.append(np.nan)
                        else:
                            row.append(elem.text)
                    elif elem.name == 'th':
                        row.append(-999.99)
            rows.append(row)         
    
    return rows

def to_dataframe(list):
    df = pd.DataFrame(columns=['year', 'station', 'lev_type', 'day', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    for d in list:
        for r in d:
            df.loc[len(df)] = r
    return df