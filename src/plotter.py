import time

#used to get data from a directory
import os
from os import listdir
from os.path import isfile, join

from settings import *
from librarian import *
from clerk import *



def mplfinance_plot(ticker, chart_type, syear, smonth, sday, eyear, emonth, eday):
    start = f"{syear}-{smonth}-{sday}"
    end = f"{eyear}-{emonth}-{eday}"
    try:
        df = pd.read_csv("~/progetti/Finance/archive/" + ticker + ".csv")
    except FileNotFoundError:
        print("File doesn't exist")
    else:
        df.index = pd.DatetimeIndex(df['Date'])
        df_sub = df.loc[start:end]
        #candlestick
        mpf.plot(df_sub, type='candle', title="candlestick")
        #price change line
        mpf.plot(df_sub, type='line', title="price change line")
        #moving average
        mpf.plot(df_sub, type='ohlc', mav=4, title="moving average")
        
        #styles
        s =mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size':8})
        fig = mpf.figure(figsize=(12,8), style=s)

        #subplots
        ax = fig.add_subplot(2,1,2)
        av = fig.add_subplot(2,1,2, sharex=ax)
        mpf.plot(df_sub, type=chart_type, mav=(3,5,7), ax=ax, volume=av, show_nontrading=True)



def price_plot(ticker,syear, smonth, sday, eyear, emonth, eday):
    start = f"{syear}-{smonth}-{sday}"
    end = f"{eyear}-{emonth}-{eday}"
    try:
        df = pd.read_csv("~/progetti/Finance/archive/" + ticker + ".csv")
    except FileNotFoundError:
        print("File doesn't exist")
    else:
        df.index = pd.DatetimeIndex(df['Date'])
        df_sub = df.loc[start:end]
        df_np = df_sub.to_numpy()
        np_adj_close = df_np[:,5]
        date_arr = df_np[:,1]
        fig = plt.figure(figsize=(12,8), dpi=100)
        axes = fig.add_axes([0,0,1,1])
        axes.plot(date_arr, np_adj_close, color="navy")
        axes.xaxis.set_major_locator(plt.MaxNLocator(8))
        axes.grid(True, color="0.6", dashes=(5,2,1,2))
        axes.set_facecolor("#FAEBD7")        