from output import color_output

# get file list in dir with sorting descending way
def file_list(path, reverse_or_not):
    import os
    file_list=os.listdir(path)
    file_list.sort(reverse=reverse_or_not)
    for file in file_list:
        if(file==".git/"):
            file_list.remove(".git/") # remove unwanted file
        if(file=="README.md"):
            file_list.remove("README.md")
    return file_list

def file_line_count(file1):
    count=0
    for row in open(file1): 
        count += 1
    return count

# get file data with tuple in list in a single file
def file_data(file1):
    with open(file1, 'r') as f:
        file_data=f.readlines()
        for idx in range(file_line_count(file1)):
            file_data[idx]=file_data[idx].strip("\n").split("/")
        f.close()
    return file_data

# get all data files to read-only mode
def read_only(file_path):
    import os
    files=file_list(file_path, False)
    os.chdir(file_path)
    for file1 in files:
        if(file1!=".git" and file1!="README.md"):
            os.chmod(file1, 0o444) # 0o means octal representation
    return

# get all data files to read-write mode
def read_n_write(file_path):
    import os
    files=file_list(file_path, False)
    os.chdir(file_path)
    for file1 in files:
        if(file1!=".git" and file1!="README.md"):
            os.chmod(file1, 0o664) # 0o means octal representation
    return

# get integer only used in getting openfilenumbers & presenting columnsize
# int_limit is used for filenumber valid or not(-1 means no limit)
def input_integer(line, int_limit):
    while(True):
        color_output("purple", str(line), False)
        ans=input("")
        # contains non-digit component
        if(ans.isdigit()==False):
            color_output("red" "[ERROR] contains non-digit symbol\n", True)
        # exceed limit
        elif(int_limit!=-1 and int(ans)>int(int_limit)):
            color_output("red", "[ERROR] exceed limitation\n", True)
        else:
            return ans
    return

# get column name based on the given filenumber
def openfile_name(path, filenumber):
    files=file_list(path, False)
    return str(files[int(filenumber)-1])

# get_slope will receive two parameter
# first one is NEWER data, and the second one is OLDER data
# the slope will be NEWER-OLDER, and based on the result, return result
# result 1: positive slope; 0: slope=0; -1: negative slope
def get_slope(new_data, old_data):
    if new_data-old_data>0:
        return 1
    elif new_data-old_data==0:
        return 0
    elif new_data-old_data<0:
        return -1

# this function received filedata_list && given stock id,
# return the stock id's high & low price as list
# If NOT EXIST, return both 'NaN'
def stock_data(filedata_list, stockid):
    for stock in filedata_list:
        # find matched stock, return result
        if str(stock[0])==str(stockid):
            result=[str(stock[1]), str(stock[2])]
            return result
    # if run through all stock, no matched stock id
    result=["NaN", "NaN"]
    return result
