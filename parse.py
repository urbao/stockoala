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

#-------------------------------------------------#

# unlock all files to writable, and get most recent date for checking
get.read_n_write(datapath)
# True means reverse the data file list
# So, the first filename is the latest one
filelist=get.file_list(datapath, True)
print(filelist)
    
# use file list grab data for analyze(file list: DESCENDING sort)


# Finally, let all files to read-only for safety
get.read_only(datapath)
