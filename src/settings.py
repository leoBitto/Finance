import datetime as dt

PATH = "/home/leonardo/progetti/Finance/archive/"
PATH_to_stock = "/home/leonardo/progetti/Finance/src/stocks/big_stock_sectors.csv"

S_YEAR = 2009
S_MONTH = 1
S_DAY = 1
S_DATE_STR = f"{S_YEAR}-{S_MONTH}-{S_DAY}"
S_DATE_DATETIME = dt.datetime(S_YEAR, S_MONTH, S_DAY)

E_YEAR = 2022
E_MONTH = 3
E_DAY = 27
E_DATE_STR = f"{E_YEAR}-{E_MONTH}-{E_DAY}"
E_DATE_DATETIME = dt.datetime(E_YEAR, E_MONTH, E_DAY)
