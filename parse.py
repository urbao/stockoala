"""
Analyze Method: from thisweek and traceback to past
If the move "reverse-point" occurs in this week, which means there must exist a valley point
in the past few week, and another peak point much long ago than valley point .So, try to use the slope of HIGH and LOW data to analyze
"""

import get, os 
#-------Path Definition(DO NOT MODIFY)------------#
# dirpath: used to store result file
# datapath: used to get data list for analyzing

datapath="/home/eason/Desktop/stockoala/data/"
parse_max_depth=10

#-------------------------------------------------#
# enable write and read files
get.read_n_write(datapath)

# True means reverse the data file list
# So, the first filename is the latest one
filename_list=get.file_list(datapath, True)

# initialize a list array, and stored recent 10 weeks data based on 
# filename_list into filedata_arr
import numpy as np
filedata_arr = [np.array([]) for _ in range(parse_max_depth)]
for i in range(parse_max_depth):
    filedata_arr[i]=get.file_data(filename_list[i])

# filedata_arr[0] means the latest data, basically it should be this week's data store in list type
# all analyze should only consider those on the list
for stock in filedata_arr[0]:
    if(stock[2]=="--" or stock[2]=="----"):
        print(stock)

print(get.stock_data(filedata_arr[0], 2330))
print(get.stock_data(filedata_arr[0], 1562))
print(get.stock_data(filedata_arr[0], 2230))

# lock datafiles for safety
get.read_only(datapath)

