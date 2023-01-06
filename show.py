# this script used to show datafiles content
# used ref: output.py for showing result
# used ref: get.py for getting user's input of col_size && open_filename
import os
import output
import get

filenumber=get.input_integer("Enter file number:", int(len(get.file_list("/home/eason/Desktop/@stockoala/data", False))))
filename=get.openfile_name("/home/eason/Desktop/@stockoala/data", filenumber)
columnsize=get.input_integer("Enter column size:", -1) # no column count limit, based on personal's screen width
os.chdir("data/")
output.file_content(filename, columnsize)
