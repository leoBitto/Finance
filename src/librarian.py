###############################################
##
## Librarian is a module of python for finance
##  program. 
## It takes care of the archive folder: 
##  it download the data,
##  clean it up, 
##  create dataframe from csv files,
##
##
## Author : Leonardo Bitto
###############################################


#%matplotlib inline
#for defining dates
import datetime as dt
import time
from os import listdir
from os.path import isfile, join

#styling dates
import matplotlib.dates as mdates
#plotting
import matplotlib.pyplot as plt
#matplotlib finance
import mplfinance as mpf
#provides ways to work with large multidimensional arrays
import numpy as np
#allows for further data manipulation and analysis
import pandas as pd
#read stock data
from pandas_datareader import data as web

from src.settings import *


stocks_not_downloaded = []
missing_stocks = []
# check archive folder and list all the csv files there
#[:-4] needed to eliminate file extension
tickers = [x[:-4] for x in listdir(PATH) if isfile(join(PATH, x))]
companies_df = pd.read_csv(PATH_to_stock)
sectors = companies_df.Sector.unique()

################ DATA CLEANUP
#############################
## function that clean the data
def delete_unnamed_cols(df):
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

#DATAFRAME PRESENTING DATA IN A TIME WINDOWS, between two dates
#the market is closed in the weekend so its natural to be 
#'holes' in the data
def get_valid_dates(df, sdate, edate):
    try:
        mask = (df['Date'] > sdate) & (df['Date'] < edate)
        # smaller dataframe is the dataframe limited by the dates searched
        smaller_df = df.loc[mask]
        smaller_df = smaller_df.set_index(['Date'])
        #choose cosest dates to the one searched
        start_valid_date = smaller_df.index.min()
        end_valid_date = smaller_df.index.max()
        ## add leading zeroes
        date_start = '-'.join(('0' if len(x) < 2 else '')+x for x in start_valid_date.split('-'))
        date_end = '-'.join(('0' if len(x) < 2 else '')+x for x in end_valid_date.split('-'))
    except Exception:
        print('Date corrupted')
        
    else:
        return date_start, date_end


############### DATAFRAME HANDLING save/get/add daily return
##################################
def get_df_from_csv(ticker):
    today_date = dt.datetime.today()
    try:
        #look for the dataframe in the Archive folder
        df = pd.read_csv(PATH + ticker + ".csv", index_col = 'Date', parse_dates=True)
        df = delete_unnamed_cols(df)
        # control if it is updated
        date_end = df.index.max().to_pydatetime()
        

        if date_end.date() < today_date.date():
            try:  #to update the csv
                print("Updating to today date for :", ticker)
                updated_df = web.DataReader(ticker, 'yahoo', date_end, today_date)
                updated_df = delete_unnamed_cols(updated_df)

                time.sleep(3)

                new_df = pd.concat([df, updated_df])
                new_df = delete_unnamed_cols(new_df)
                new_df = new_df[~new_df.index.duplicated()]
                # save the new updated df
                new_df.to_csv(PATH + ticker + ".csv")
                print(ticker, "has been updated and saved in ", PATH)

            except Exception as ex:
                print("Couldn't get updated data for :", ticker)
                print("ERROR: ", ex)

    except FileNotFoundError:
        print("File doesn't exist, I'll try to download it...")
        save_to_csv_from_yahoo(ticker, S_DATE_DATETIME, today_date)
        
    else:
        fdf = pd.read_csv(PATH + ticker + ".csv", index_col = 'Date', parse_dates=True)
        fdf = add_daily_return_to_df(fdf)
        return fdf

def save_df_to_csv(df, ticker):
    df.to_csv(PATH + ticker + '.csv')

# return a dataframe column from a csv
def get_column_from_csv(ticker, col_name):
    df = get_df_from_csv(ticker)
    return df[col_name]

def get_column_between_dates(ticker, col_name, sdate, edate):
    df = get_column_from_csv(ticker, col_name)
    mask = (df.index >= sdate ) & ( df.index <= edate )
    return df.loc[mask]

#merge multiple stocks in dataframe by column name
def merge_df_by_column_name(col_name, sdate, edate, *tickers):
    mult_df = pd.DataFrame()

    try:
        for x in tickers:
            df = get_df_from_csv(x)
            mask = (df.index >= sdate ) & ( df.index <= edate )
            mult_df[x] = df.loc[mask][col_name]
    except Exception as e:
        print("There was a problem merging the data, probably the number of days didn't match")
        print("Try a more recent date for the beginning.")
        print("ERROR MESSAGE", e)
    else:
        return mult_df

#we calculate a percentage rate of return for each day to compare investments
#simple rate of Return = (End Price - Beginning Price) / Beginning Price OR (EP / BP) - 1
def add_daily_return_to_df(df):
    df["daily_return"] = (df['Adj Close'] / df['Adj Close'].shift(1)) - 1
    return df


################# DOWNLOADER
############################
def save_to_csv_from_yahoo(ticker, sdate, edate):
    try:
        print("Getting Data for :", ticker)
        df = web.DataReader(ticker, 'yahoo', sdate, edate)
        df = delete_unnamed_cols(df)
        #df = add_daily_return_to_df(df)
        time.sleep(7)
        df.to_csv(PATH + ticker + ".csv")
        print("Added : ", ticker, " to ", PATH)
    except Exception as ex:
        stocks_not_downloaded.append(ticker)
        print("Couldn't get data for :", ticker)
        print(ex)

##DOWNLOAD MULTIPLE STOCK
# try to download all the stocks then try again with the one 
# that it didn't manage to download
def download_multiple_stocks(stocks_list, sdate, edate):
    print(stocks_list)
    for x in stocks_list:
        save_to_csv_from_yahoo(x, sdate, edate)
    print("Finished!!")
    
    print("I didn't manage to download these... ", stocks_not_downloaded, "I'll try again!")
    for x in missing_stocks:
        save_to_csv_from_yahoo(x, sdate, edate)
    print("Finished!!")
    print("These couldn't be downloaded: ", stocks_not_downloaded)




