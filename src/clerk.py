#################################################
##
## Clerk is a piece of software to calculate 
##  statistics between dates of a time series
##  of days of trade of several stocks
##  the software can be used to create optimal
##  portfolios. 
## The dataof a single stok is gathered by the 
##  librarian module, while Clerk operates on
##  the single stocks
##
## Author : Leonardo Bitto
#################################################

from src.settings import *
from src.librarian import *

#### BASIC STATS BETWEEN DATES OF 'Adj. Close'
#### OF A SINGLE STOCK given its dataframe
####    they return single values
### MEAN
def get_mean_between_dates(df, sdate, edate):
    try:
        mask = (df['Date'] >= sdate) & (df['Date'] <= edate)
        mean = df.loc[mask]['Adj Close'].mean()
    except Exception:
        print("Date corrupted")
    else:
        return mean
### STANDARD DEVIATION
# Standard deviation is a measure of the amount of variation within a seto of values. 
# A low standard deviation indicates that the values thend to be close to the mean. 
# A high standard deviation means values are more spread out.
# To get the standard deviation find the square root of the variation
# risk is a measure of the variability of return.
# Variance and standard deviation allow us to quantify risk.

# #### Variance
# Variance is a measure of how spread out a dataset is .
# it is calculated as the average squared deviation of each number from the mean of a dataset.
# it equals the sum of the squares of the difference between 
# each data point and the mean divided by the number of data points minus 1

# Example: if we have 3 anual returns of 23%, -8% and 15%. 
# the mean return is 10%.
def get_std_between_dates(df, sdate, edate):
    try:
        mask = (df['Date'] >= sdate) & (df['Date'] <= edate)
        std = df.loc[mask]['Adj Close'].std()
    except Exception:
        print("Date corrupted")
    else:
        return std
### COEFFICIENT OF VARIATION CV
def get_cv_between_dates(df, sdate, edate):
    mean = get_mean_between_dates(df, sdate, edate)
    std = get_std_between_dates(df, sdate, edate)
    return std/mean


#### GET INDEXES, return single values
### ROI
#### Return total return over time 
#Return On Investment is the return you received from your investment
# this amount does not include your initial investment
#
#if you invest 100 and have 200 after 5 years:
# * ROI = End Value (200) - Initial Value (100) / Initial Value = 1
# * your new total is Initial Investment + 1 * Initial Investment = 200
def get_roi_between_dates(df, sdate, edate):
    try:
        df = get_column_between_dates(df, 'Adj Close', sdate, edate)
        start_val = df.max()
        end_val = df.min()
        print(start_val, end_val)
        roi = ((end_val - start_val)/start_val)    
    except Exception as e:
        print("Date Corrupted")
        print("ERROR MESSAGE: ", e)
    else:
        return roi
###


#### STATS FOR MULTIPLE STOCKS FOR THE SAME PERIOD OF TIME
#### given a list of tickers, search for their csv
#### and calculate CV and ROI
#### return a dataframe
def get_cv_roi(tickers, sdate, edate):
    col_name = ['Ticker', 'CV', 'ROI']
    df = pd.DataFrame(columns=col_name)
    for ticker in tickers:
        s_df = get_df_from_csv(ticker)
        sdate2, edate2 = get_valid_dates(s_df, sdate, edate)
        cv = get_cv_between_dates(s_df, sdate2, edate2)
        roi = get_roi_between_dates(s_df, sdate2, edate2)
        df.loc[len(df.index)] = [ticker, cv, roi]
    return df


### CORRELATION OF A PORTFOLIO daily returns between dates
# CORRELATION TELLS US HOW CLOSELY RETURNS OF 2 STOCKS MOVE TOGETHER  
# CORRELATION IS A STANDARDIZED VALUE THAT VARY FROM -1 AND 1 , SO IT  
# TELLS US ALSO WHICH DIRECTION THE TWO RETURN GO, IF -1 ONE GOES UP
# THE OTHER THE OPPOSITE, WHEN 1 THEY BOTH GO IN THE SAME DIRECTION  
# WHEN THE CORRELATION VALUE IS GREATER THAT .5 WE SAY THE TWO STOCKS  
# ARE STRONGLY CORRELATED. EVERY STOCK PRICE IS PERFECTLY CORRELATED WITH  
# ITSELF.  
# WE FOCUS ON CORRELATION ON RETURNS BECAUSE AS INVESTORS WE CARE ABOUT RETURNS
def get_port_corr(sdate, edate, *stocks):
    return merge_df_by_column_name('daily_return', sdate, edate, *stocks).corr()


### COVARIANCE OF A PORTFOLIO daily returns between dates
### it is a dataframe that contain the variance/covariance
### matrix THESE CALCULATION ARE DONE WITH ALL THE WITH EQUIVALENT WEIGHTS
def get_port_cov(sdate, edate, *stocks):
    return merge_df_by_column_name('daily_return', sdate, edate, *stocks).cov()



############### PORTFOLIO CREATION AND MANAGEMENT
############ aggregate a portfolio, it is a list of tuples
######### the first value of a tuple is the ticker
###### the second value is the amount invested

### Analyze risk and returns
## different types  of risks:
# there is risk you can limit through diversification (idiosyncratic) and risk that you cant(systematic). Systematic risk is caused by unforeseen conditions sucj as wars, recessions natural dissters etc...  
# data tells us that if we make a portfolio made up of approximately 25 stocks that arent correlated then we can dramatically lower idisyncratic risk. this is the reason people invest in indexes.  
# you can further lower risk by investing in other countries, bonds, and cash

def get_roi_between_dates(ticker, sdate, edate):
    df = get_column_between_dates(ticker, 'Adj Close', sdate, edate)
    initial_value = df.iloc[0]
    end_value = df.iloc[-1]
    return (end_value - initial_value)/initial_value

def get_roi_for_industry(tickers_industry, sdate, edate):
    tickers = []
    rois = []
    for index, row in tickers_industry.iterrows():
        ticker = row['Ticker']
        tickers.append(ticker)
        roi = get_roi_between_dates(ticker, sdate, edate)
        print(ticker, roi)
        rois.append(roi)
        
    return pd.DataFrame({'Tickers':tickers, 'ROIs':rois})


# get best in each sectors
def get_best_in_sectors(sectors, sdate, edate):
    sec_df = pd.read_csv(PATH_to_stock)
    for sector in sectors:
        best_for_sector = []
        secTickROI = pd.DataFrame()
        sector_df = sec_df.loc[sec_df['Sector'] == sector]
        secTickROI.append({'Sector':sector, 'tickers_rois':get_roi_for_industry(sector_df,sdate,edate)})

        best_for_sector.append(secTickROI[sector].sort_values(by=['ROI'], ascending=False)[0])

    return merge_df_by_column_name('daily_return', sdate, edate, *best_for_sector)

