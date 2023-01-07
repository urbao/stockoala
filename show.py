# this script used to show datafiles content
# used ref: output.py for showing result
# used ref: get.py for getting user's input of col_size && open_filename
import os
import output
import get


# address definition
#-----DO NOT MODIFY-----#
dirpath="/home/eason/Desktop/stockoala/"

dirpath="/home/eason/Desktop/stockoala/"

dirpath="/home/eason/Desktop/stockoala/"


#-----DO NOT MODIFY-----#

filenumber=get.input_integer("Enter file number:", int(len(get.file_list(str(dirpath)+"data", False))))
filename=get.openfile_name(str(dirpath)+"data", filenumber)
columnsize=get.input_integer("Enter column size:", -1) # no column count limit, based on personal's screen width
os.chdir(str(dirpath)+"data")
output.file_content(filename, columnsize)

