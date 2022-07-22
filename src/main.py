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
    sdate = '2015-01-01'
    edate = dt.datetime.today().strftime('%Y' + '-' + '%m' + '-' + '%d')
    print(get_best_in_sectors(sectors, sdate, edate))

if __name__ == '__main__':
    main()