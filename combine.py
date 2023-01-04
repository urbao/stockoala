from output import color_output
from date_time import add_1day

# return how many lines in the specific file
def file_line_count(filename, filetype):
    line_count=0
    for row in open(filename+"["+filetype+"].txt"): line_count += 1
    return line_count

# run through all file1, check if the curr_line of file2 exist in file 1
def matched_id_in_file1(file1, curr_line, line_count1):
    for idx in range(line_count1):
        if(file1[idx][0]==curr_line[0]):
            return idx
    return -1

# curr_line is current id of file2
# file1 is all data in file1
# need to consider NaN situation(-- and ----)
# return the final list with id, high, low, respectively
def cmpare_2day_same_id(file1, curr_line, line_count1):
    # case1: curr_line id only exist in file2, return and write directly
    idx=matched_id_in_file1(file1, curr_line, line_count1)
    if(idx==-1):
        return curr_line
    # case2: data in curr_line or file1[idx] is NaN
    if(file1[idx][1]=="--" or file1[idx][1]=="----"):
        return curr_line
    if(curr_line[1]=="--" or curr_line[1]=="----"):
        return file1[idx]
    # case3: compare two days data and return result
    result=['id_value', 'high_price', 'low_price']
    result[0]=file1[idx][0]
    result[1]=str(max(float(file1[idx][1].replace(',', '')), float(curr_line[1].replace(',', ''))))
    result[2]=str(min(float(file1[idx][2].replace(',', '')), float(curr_line[2].replace(',', ''))))
    return result

# return the file as list type with unwanted symbols removed
def get_file_as_list(filename, filetype, file_line_count):
    with open(filename+"["+filetype+"].txt", 'r') as f:
        file=f.readlines() # read all lines as list array at once
        for idx in range(file_line_count): # run all line 
            file[idx]=file[idx].strip("\n").split("/") # rm extra symbols
        f.close()
    return file

def cmbine_2day(filename1, filename2, filetype):
    # ALWAYS use FILE1 as REFERENCE
    # read file1 at once, and store into file1(list array)
    file1_line_count=file_line_count(filename1, filetype)
    file2_line_count=file_line_count(filename2, filetype)
    file1=get_file_as_list(filename1, filetype, file1_line_count)
    # read file2 line by line
    # if some id in file2 no match id in file1, then append data to file1
    with open(filename1+"["+filetype+"].txt", 'w') as f1:
        with open(filename2+"["+filetype+"].txt", 'r') as f2:
            for i in range(file2_line_count):
                curr_line=f2.readline().strip("\n").split("/")
                result=cmpare_2day_same_id(file1, curr_line, file1_line_count)
                f1.write(result[0]+"/"+result[1]+"/"+result[2]+"\n")
            f2.close()
        f1.close()
    import os
    os.remove(filename2+"["+filetype+"].txt") # no need for file2
    # Final check(EXCEPTION: when file1 list exist, while no same id data in file2)
    # Re-check if every id in file1 list appears in file1(get new_file1 list)
    # If not, append the data to file1
    new_file1_line_count=file_line_count(filename1, filetype)
    new_file1=get_file_as_list(filename1, filetype, new_file1_line_count)
    with open(filename1+"["+filetype+"].txt", 'a') as f1:
        for idx in range(file1_line_count):
            if(matched_id_in_file1(new_file1, file1[idx], new_file1_line_count)==-1):
                f1.write(file1[idx][0]+"/"+file1[idx][1]+"/"+file1[idx][2]+"\n")
        f1.close()
    return

def weekly_data(start_date, filetype, period_length):
    # use iteration to find weekly data(TWSE and TPEX)
    color_output("purple", "Parsing", False)
    if(filetype=="twse"):
        color_output("yellow", "TWSE", False)
    else:
        color_output("cyan", "TPEX", False)
    color_output("purple", "data", False)
    date=start_date
    next_date=date
    for i in range(period_length): # THE 4 CAN CHANGED TO ANY LENGTH OF DAYS AS WE WANT
        next_date=str(add_1day(next_date))
        cmbine_2day(date, next_date, filetype)
    import os
    if(os.stat(start_date+"["+filetype+"].txt").st_size==0):
        color_output("red", "[FAIL]", True) 
    else:
        color_output("green", "[DONE]", True) 

# use for sorting via stock id 
def id_sort(line):
    amount=int(line[0])
    return amount

# combine TWSE and TPEX together as a file
def final_combine(date):
    color_output("purple", "Combining data", False)
    twse_count=file_line_count(date, "twse")
    tpex_count=file_line_count(date, "tpex")
    twse=get_file_as_list(date, "twse", twse_count)
    tpex=get_file_as_list(date, "tpex", tpex_count)
    total=twse+tpex
    import os
    os.remove(date+"[twse].txt")
    os.remove(date+"[tpex].txt")
    if(len(total)==0):
        color_output("red", "[FAIL]", True)
    else:
        color_output("green", "[DONE]", True)
    color_output("purple", "Sorting by stock id", False)
    total.sort(key=id_sort)
    with open(date+"[total].txt", 'w') as f:
        for idx in range(twse_count+tpex_count):
            f.write(total[idx][0]+"/"+total[idx][1]+"/"+total[idx][2]+"\n")
    f.close()
    total_count=file_line_count(date, "total")
    count=[twse_count, tpex_count, total_count]
    if(len(total)==0):
        color_output("red", "[FAIL]", True)
    else:
        color_output("green", "[DONE]", True)
    return count
