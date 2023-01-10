# get.py used to implement some useful function
# like request, date, prune, combine...

# request for data(return True: has data needed to prune/ False: Nvm)
# TWSE Case
# use urllib module to retrieve TWSE specific day's data(including code/name/open/high/low/close)
def twse(date):
    from output import color_output
    color_output("purple", "Request", False)
    color_output("yellow", str(date)+" TWSE", False)
    color_output("purple", "data", False)
    from urllib import request
    URL="https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date="+str(date)+"&type=ALL"
    request.urlretrieve(URL, str(date)+"[twse].json")
    # check if files is no data
    with open(str(date)+"[twse].json", 'r') as j:
        import json
        content=json.loads(j.read())
        if(content['stat']=="很抱歉，沒有符合條件的資料!"): # no data stored
            color_output("red", "[FAIL]", True)
            return False
        else:
            color_output("green", "[PASS]", True)
            return True

# TPEX Case
def tpex(date):
    from output import color_output
    color_output("purple", "Request", False)
    color_output("cyan", str(date)+" TPEX", False)
    color_output("purple", "data", False)
    # generate random timstamp for url
    from datetime import datetime
    curr_t = datetime.now()
    time_stamp = datetime.timestamp(curr_t)
    # find current date for url(based on url date format)
    from urllib import request
    serch_date=str(int(date[0:4])-1911)+"/"+date[4:6]+"/"+date[6:8]
    URL="https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&d="+str(serch_date)+"&se=AL&_="+str(time_stamp*1000)
    request.urlretrieve(URL, str(date)+"[tpex].json")
    # check if files is no data
    with open(str(date)+"[tpex].json", 'r') as j:
        import json
        content=json.loads(j.read())
        if(content['iTotalRecords']==0): # no data stored
            color_output("red", "[FAIL]", True)
            return False
        else:
            color_output("green", "[PASS]", True)
            return True

# Prune for TWSE
def twse_prune(filename):
    with open(filename+"[twse].json", 'r') as j:
        import json
        alldata=json.loads(j.read())
        data=alldata['data9']
        f=open(filename+"[twse].txt",'w')
        for idx in range(len(data)):
            if len(data[idx][0])==4: # prune those whose id is longer than 4 digit
                if int(data[idx][0])>1000: # prune those whose
                    f.write(str(data[idx])+"\n")
        f.close()
    j.close()
    import os
    os.remove(filename+"[twse].json")
    return

# Prune for TPEX
def tpex_prune(filename):
    with open(filename+"[tpex].json", 'r') as j:
        import json
        alldata=json.loads(j.read())
        data=alldata['aaData']
        f=open(filename+"[tpex].txt",'w')
        for idx in range(int(alldata['iTotalRecords'])):
            if len(data[idx][0])<5:
                f.write(str(data[idx])+"\n")
        f.close()
    j.close()
    import os 
    os.remove(filename+"[tpex].json")
    return

# Date Configuration
# check if date is valid
def valid_date(chk_date):
    from output import color_output
    from datetime import datetime, date
    if(len(chk_date)!=8): # date too long or short
        color_output("red", "[ERROR] Invalid Format\n", True)
        return False
    try: # error when trying convert to date object
        dateObj=datetime.strptime(chk_date, '%Y%m%d')
    except ValueError:
        color_output("red", "[ERROR] Invalid Date\n", True)
        return False
    # check if it's Monday
    if(date(int(chk_date[0:4]), int(chk_date[4:6]), int(chk_date[6:8])).weekday()==0):
        return True
    else:
        color_output("red", "[ERROR] Not Monday\n", True)
        return False

# get start date input from user         
def date_from_user():
    from output import color_output
    # show reminder
    color_output("cyan", "-- Date Example: 20220320 and 20011009", True)
    color_output("cyan", "-- Period Example(days): 5 and 6", True)
    color_output("red", "-- [FAIL] means data NOT collected or parsed\n",True)
    while(True):
        color_output("white", "Enter Date:", False)
        date=input("")
        if(valid_date(date)):
            return date

# get date based on given timedelta
# if delta negative, then the date will be past
# if delta positive, then the date will be future
def date_with_given_delta(date, delta):
    from datetime import datetime
    from datetime import timedelta
    curr_date=datetime.strptime(date, '%Y%m%d')
    result=str(curr_date+timedelta(int(delta)))
    year=str(result[0:4])
    month=str(result[5:7])
    day=str(result[8:10])
    return year+month+day

# get usr desired stock data collected period length
def period_length_from_user():
    from output import color_output
    while(True):
        color_output("white", "Enter Period:", False)
        period=input("")
        if(period.isdigit()): # check if only digit(NO negative sign or others allowed)
            if(int(period)>0): # period can not be 0 days
                return period
            else:
                color_output("red", "[ERROR] Period can NOT be 0 day\n", True)
        else:
            color_output("red", "[ERROR] contains non-digit symbol\n", True)

# Combine Stock data
# return how many lines in the specific file
def file_line_count(filename, filetype):
    line_count=0
    for row in open(filename+"["+filetype+"].txt"): 
        line_count += 1
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
            file[idx]=file[idx].strip('\n').strip('][').split(', ') # rm extra symbols
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

# Parse weekly data for TWSE & TPEX, respectively
def weekly_data(start_date, filetype, period_length):
    from output import color_output
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
        next_date=str(date_with_given_delta(next_date))
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
    from output import color_output
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





twse("20230109")
twse_prune("20230109")
with open("20230109"+"["+"twse"+"].txt", 'r') as f:
    file=f.readlines() # read all lines as list array at once
    flc=file_line_count("20230109", "twse")
    for idx in range(flc): # run all line 
        file[idx]=file[idx].strip('\n').strip('][').split(', ') # rm extra symbols
        print(file[idx][0])
    f.close()
