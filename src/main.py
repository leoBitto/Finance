#!/usr/bin/env python3

import time

#used to get data from a directory
import os
from os import listdir
from os.path import isfile, join

from settings import *
from librarian import *
from clerk import *

def main():
    ticker = input("what stock do you want? : ")
    df = get_df_from_csv(ticker)
    print(df)

if __name__ == '__main__':
    main()