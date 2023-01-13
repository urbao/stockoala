# get.py used to implement some useful function
# like request, date, prune, combine...

# --------------------------request for data-----------------------------
# (return True: has data needed to prune/ False: Nvm)
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
# --------------------------Prune stock data---------------------------------
# RESULT FORMAT: ID|HIGH|LOW|OPEN|CLOSE|TRANSACTION
# Prune for TWSE(id/name/trade volume/transaction/trade value/open/high/low/close)
def twse_prune(filename, twse_stats):
    import os
    with open(filename+"[twse].json", 'r') as j:
        import json
        alldata=json.loads(j.read())
        f=open(filename+"[twse].txt",'w')
        if twse_stats==False:
            pass
        else:
            data=alldata['data9']
            for idx in range(len(data)):
                if len(data[idx][0])==4: # prune those whose id is longer than 4 digit
                    if int(data[idx][0])>1000: # prune those whose
                        ID=str(data[idx][0])
                        Transaction=str(int(int(data[idx][2].replace(',', ''))/1000)) # use trade share to calc trade count
                        Open=str(data[idx][5])
                        High=str(data[idx][6])
                        Low=str(data[idx][7])
                        Close=str(data[idx][8])
                        line="["+ID+", "+High+", "+Low+", "+Open+", "+Close+", "+Transaction+", tse]"
                        f.write(line+"\n")
        f.close()
    j.close()
    os.remove(filename+"[twse].json")
    return

# Prune for TPEX(id/name/close/change/open/high/low/trade volume/trade amount/transaction)
def tpex_prune(filename, tpex_stats):
    import os 
    with open(str(filename)+"[tpex].json", 'r') as j:
        import json
        alldata=json.loads(j.read())
        f=open(str(filename)+"[tpex].txt",'w')
        if tpex_stats==False:
            pass
        else:
            data=alldata['aaData']
            for idx in range(int(alldata['iTotalRecords'])):
                if len(data[idx][0])<5:
                    ID=str(data[idx][0])
                    Transaction=str(int(int(data[idx][7].replace(',', ''))/1000)) # use trade share to calc trade count
                    Open=str(data[idx][4])
                    High=str(data[idx][5])
                    Low=str(data[idx][6])
                    Close=str(data[idx][2])
                    line="["+ID+", "+High+", "+Low+", "+Open+", "+Close+", "+Transaction+", otc]"
                    f.write(line+"\n")
        f.close()
    j.close()
    os.remove(str(filename)+"[tpex].json")
    return
# --------------------------Combine & Get stock data---------------------------------
# Combine TWSE & TPEX data of same day into one file named $date.txt
def merge_same_day_data(date):
    stock_data=[]
    with open(str(date)+"[twse].txt", 'r') as twse:
        twse_data=twse.readlines()
        for idx in range(len(twse_data)):
            twse_data[idx]=twse_data[idx].strip('\n').strip('][').split(', ')
            stock_data.append(twse_data[idx])
    twse.close()
    with open(str(date)+"[tpex].txt", 'r') as tpex:
        tpex_data=tpex.readlines()
        for idx in range(len(tpex_data)):
            tpex_data[idx]=tpex_data[idx].strip('\n').strip('][').split(', ')
            stock_data.append(tpex_data[idx])
    tpex.close()
    # sort the stock_data by the stock id,
    # and return the result as a 2D-list
    stock_data=sorted(stock_data, key=lambda l: l[0])
    import os
    os.remove(str(date)+"[twse].txt")
    os.remove(str(date)+"[tpex].txt")
    return stock_data

# find weekly total stock id from period_data_list
# return a list contains all valid stock id of this week
def stockid_list(period_data_list):
    # if the item is empty, ignore
    # if not, then compare each day data_list with the current result, see if some id is missing
    # store all current valid stock id
    result=['0000'] # not empty list, so for-loop will go in, and append missing stockid
    for day in range(len(period_data_list)): # run through every day's data
        for idx in range(len(period_data_list[day])): # run through all stock id for every day
            for i in range(len(result)): # run through all stored id in result
                if str(result[i])==str(period_data_list[day][idx][0]): # matched id, so break the loop, goto next idx
                    break
                elif i==len(result)-1: # already reach last i, still no matched
                    result.append(str(period_data_list[day][idx][0])) 
    result=sorted(result)
    result.remove('0000')
    return result

# find the Max/min of given stockid in period_data_list
# stockid: only one stock, ex: 1101, 2230....
# type: 'Max' or 'min'
def stock_period_max_min(period_data_list, stockid, type):
    period_data=[]
    for day in range(len(period_data_list)): # run through all day
        for idx in range(len(period_data_list[day])): # run through all idx to see if match id
            if str(period_data_list[day][idx][0])==str(stockid):
                # add one more check preventing from receiving some non-float data
                if period_data_list[day][idx][1]=="--" or period_data_list[day][idx][1]=="----":
                    pass
                elif type=='Max':
                    period_data.append(float(period_data_list[day][idx][1].replace(',', '')))
                elif type=='min':
                    period_data.append(float(period_data_list[day][idx][2].replace(',', '')))
    if len(period_data)==0: # whole period has No valid data, so mark as 'NaN', when analyze ignore
        return "NaN"
    elif type=='Max':
        return str(max(period_data))
    else:
        return str(min(period_data))

# find period transaction of given stockid
# stockid: only one stock, ex: 1101, 2230....
def stock_period_transaction(period_data_list, stockid):
    total_transaction=0
    for day in range(len(period_data_list)):
        for idx in range(len(period_data_list[day])):
            if str(period_data_list[day][idx][0])==str(stockid): # match id case
                total_transaction+=int(period_data_list[day][idx][5].replace(',', '')) # add up transaction to total_transaction
    return str(total_transaction)

# find Open of given stockid in period_data_list
def stock_period_open(period_data_list, stockid):
    for day in range(len(period_data_list)):
        for idx in range(len(period_data_list[day])):
            if str(period_data_list[day][idx][0])==str(stockid): # matched id case
                # check if the data is valid, if NOT, break loop, and goto next day loop
                if str(period_data_list[day][idx][3])=="--" or str(period_data_list[day][idx][3])=="----":
                    break
                else:
                    return str(period_data_list[day][idx][3])
    return "NaN" # no valid data,so return a string

# find Close of given stockid in period_data_list
def stock_period_close(period_data_list, stockid):
    for day in reversed(range(len(period_data_list))): # since close price is last day, so use reversed-loop iterarion
        for idx in range(len(period_data_list[day])):
            if str(period_data_list[day][idx][0])==str(stockid): # matched id case
                # check if the data is valid, if NOT, break loop, and goto next day loop
                if str(period_data_list[day][idx][4])=="--" or str(period_data_list[day][idx][4])=="----":
                    break
                else:
                    return str(period_data_list[day][idx][4])
    return "NaN" # no valid data,so return a string

def stock_period_type(period_data_list, stockid):
    for day in range(len(period_data_list)):
        for idx in range(len(period_data_list[day])):
            if str(period_data_list[day][idx][0])==str(stockid): # match id case
                return period_data_list[day][idx][6]
    return "error"

# Use stock_period_XXXX function to find all weekly-data, then stored to file
def combine_daily_data(period_data_list, stockid_list, date):
    with open(str(date)+".txt", 'w') as file:
        for idx in range(len(stockid_list)):
            ID=str(stockid_list[idx])
            High=str(stock_period_max_min(period_data_list, ID, 'Max'))
            Low=str(stock_period_max_min(period_data_list, ID, 'min'))
            Open=str(stock_period_open(period_data_list, ID))
            Close=str(stock_period_close(period_data_list, ID))
            Transaction=str(stock_period_transaction(period_data_list, ID))
            Type=str(stock_period_type(period_data_list, ID))
            line="["+ID+", "+High+", "+Low+", "+Open+", "+Close+", "+Transaction+", "+Type+"]\n"
            file.write(line)
    file.close()
    return

# --------------------------User Input------------------------------
# get valid start date input from user         
def date_from_user():
    from output import color_output
    from datetime import datetime, date
    # show reminder
    color_output("cyan", "-- Date Example: 20220320 and 20011009", True)
    color_output("cyan", "-- Period Example(days): 5 and 6", True)
    color_output("red", "-- [FAIL] means data of that date is Empty\n",True)
    while(True):
        color_output("white", "Enter Date:", False)
        ans=input("")
        if(len(ans)!=8): # date too long or short
            color_output("red", "[ERROR] Invalid Format\n", True)
        try: # error when trying convert to date object
            dateObj=datetime.strptime(ans, '%Y%m%d')
        except ValueError:
            color_output("red", "[ERROR] Invalid Date\n", True)
        # check if it's Monday
        if(date(int(ans[0:4]), int(ans[4:6]), int(ans[6:8])).weekday()==0):
            return ans
        else:
            color_output("red", "[ERROR] Not Monday\n", True)

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

# Receive input of TWSE_index or TPEX_index based on parameter
# type can be either 'TWSE' or 'TPEX'
def index_from_user(type):
    from output import color_output
    while(True):
        color_output("white", "Enter "+str(type)+" Index(%):", False)
        ans=input("")
        try:
            ans=float(ans)
            return ans
        except:
            color_output("red", "[ERROR] Only float point number\n", True)

# --------------------------Date & Filelist Configure------------------------------
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

# get the data filelist in reverse order, so the latest will be the first file
def filename_list(filepath):
    import os
    filelist=os.listdir(str(filepath))
    filelist.sort(reverse=True)
    # run through all filename, and remove unwanted analyzed filename from the filelist
    for file in filelist:
        if(file==".git/"):
            filelist.remove(".git/")
        if(file=="README.md"):
            filelist.remove("README.md")
    return filelist

# try to read data of given filename, and return as a list datatype
def file_data(filename):
    return_data=[]
    with open(str(filename), 'r') as ff:
        data=ff.readlines()
        for idx in range(len(data)):
            data[idx]=data[idx].strip('\n').strip('][').split(', ')
            return_data.append(data[idx])

    ff.close()
    return return_data



# --------------------------Analyze Mathod and Functions------------------------------
# get slope which analyze either High or Low price of two consectutive weeks
# used to find out if a reversed-point happened or not
def slope(newdata, olddata):
    if float(newdata)-float(olddata)>0:
        return 1
    elif float(newdata)-float(olddata)==0:
        return 0
    elif float(newdata)-float(olddata)<0:
        return -1

# return stock closed price change
# formula=(thisweek_close-lastweek_close)/lastweek_close
def stock_price_change(weekdata_list, stockid):
    thisweek_close_price=0
    lastweek_close_price=0
    # find this week closed price & the last week closed price
    for week in range(len(weekdata_list)): # week: the week counter, 0 means this week, 1 means one week ago
        for stock in weekdata_list[week]: # stock: run through all stock of that specific week
            if str(stock[0])==str(stockid): # matched id
                # if this week, no closed price, then ignore it
                if stock[4]=="NaN" and week==0:
                    return -1000.0 # make sure the change will definitely smaller than INDEX of TWSE and TPEX
                elif week==0: # thisweek has valid close price
                    thisweek_close_price=float(stock[4].replace(',', ''))
                # when this happens, which means we just encounter the
                # first latest valid weekly closed price, and it's also
                # matched id, so just calculate the result, and return it
                elif week!=0 and stock[4]!="NaN":
                    lastweek_close_price=float(stock[4].replace(',', ''))
                    return round((thisweek_close_price-lastweek_close_price)/lastweek_close_price*100, 2)
                else:
                    pass
    return -1000.0 # this will happen iff the past 4 week, there's NO valid close price

# this function used to grab consectutive VALID certain stock data
def conti_valid_stock_data(weekdata_list, stockid):
    stock_data=[]
    stock_data.append(stockid) # append stock id for easier analysis
    for week in range(len(weekdata_list)):
        for stock in weekdata_list[week]:
            if str(stock[0])==str(stockid) and stock[1]!="NaN":
                high_low_price=[str(stock[1]), str(stock[2])]
                stock_data.append(high_low_price)
            else: # either NOT match id, or the data is "NaN"(NOT Valid)
                pass
    return stock_data
