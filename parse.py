"""
Analyze Method: from thisweek and traceback to past
If the move "reverse-point" occurs in this week, which means there must exist a valley point
in the past few week, and another peak point much long ago than valley point
So, try to use the slope of HIGH and LOW data to analyze
"""

import get
import output
import os

# data_file_path: weekly data stored place
data_file_path="/home/eason/Desktop/stock/data/"
# result_file_path: analysis result file stored place
result_file_path="/home/eason/Desktop/stock/"

 # unlock all files to writable, and get most recent date for checking
get.read_n_write(data_file_path)
filelist=get.file_list(data_file_path, True) # True means reverse the data file list
# remove unneccessary file name from list
filelist.remove(".git")
filelist.remove("README.md")
date=filelist[0].replace(".txt", "")
confirm=get.yes_no(date)

# Check if user want to analyze this date's data
if(confirm=="No"):
    output.color_output("white", "\nOperation Abort", True)
    get.read_only(data_file_path) # lock files before exit
    quit()
    
# use file list grab data for analyze(file list: DESCENDING sort)


# Finally, let all files to read-only for safety
get.read_only(data_file_path)
