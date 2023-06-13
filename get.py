# get.py used to implement some useful function
# like request, date, prune, combine...

# --------------------------request for data-----------------------------
# (return True: has data needed to prune/ False: Nvm)
# TWSE Case
# use urllib module to retrieve TWSE specific day's data(including code/name/open/high/low/close)
# date: used to specified certain date data
# type_code: used to append on URL for requesting correct data
# stock_type: used to show info when collecting specific class stock data
def twse(date, type_code, stock_type):
    from output import color_output
    color_output("purple", "Request", False)
    if date!="":
        color_output("yellow", str(date)+" TWSE", False)
    else:
        color_output("yellow", str(stock_type)+" of TSE", False)
    color_output("purple", "data", False)
    from urllib import request
    URL="https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date="+str(date)+"&type="+str(type_code)
    request.urlretrieve(URL, str(date)+"[twse].json")
    # check if files is no data
    with open(str(date)+"[twse].json", 'r') as j:
        import json
        content=json.loads(j.read())
        if(content['stat']=="很抱歉，沒有符合條件的資料!"): # no data stored
            color_output("red", "[FAIL]", True)
            return False
        elif(content['stat']=="查詢日期大於今日，請重新查詢!"): # no data stored
            color_output("red", "[FAIL]", True)
            return False
        else:
            color_output("green", "[PASS]", True)
            return True

# TPEX Case
def tpex(date, type_code, stock_type):
    from output import color_output
    color_output("purple", "Request", False)
    if date!="":
        color_output("cyan", str(date)+" TPEX", False)
    else:
        color_output("cyan", str(stock_type)+" OTC", False)
    color_output("purple", "data", False)
    # generate random timstamp for url
    from datetime import datetime
    curr_t = datetime.now()
    time_stamp = datetime.timestamp(curr_t)
    # find current date for url(based on url date format)
    from urllib import request
    if date!="":
        serch_date=str(int(date[0:4])-1911)+"/"+date[4:6]+"/"+date[6:8]
    else:
        serch_date="" # when parsing data, no date spcefied
    URL="https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&d="+str(serch_date)+"&se="+str(type_code)+"&_="+str(time_stamp*1000)
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
            twse_result=twse_data[idx].strip('\n').strip('][').split(', ')
            stock_data.append(twse_result)
    twse.close()
    with open(str(date)+"[tpex].txt", 'r') as tpex:
        tpex_data=tpex.readlines()
        for idx in range(len(tpex_data)):
            tpex_result=tpex_data[idx].strip('\n').strip('][').split(', ')
            stock_data.append(tpex_result)
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

# find Type of given stockid in period_data_list
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

# Receive input of TSE_INDEX or OTC_index based on parameter
# type can be either 'TSE' or 'OTC'
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

# Get the specific type of stocks needed to analyze
def tse_or_otc():
    from output import color_output
    while True:
        color_output("white", "Enter type(1.tse/2.otc):", False)
        ans=input("")
        if ans.isdigit()==True:
            if int(ans)==1:
                return "tse"
            elif int(ans)==2:
                return "otc"
            else:
                color_output("red", "[ERROR] only 1 or 2\n", True)
        else:
            color_output("red", "[ERROR] contains non-digit symbol\n", True)

# get different class of tse
def class_of_tse():
    from output import color_output
    # print out all different class of tse
    print("1.  tse全部")
    print("2.  水泥工業")
    print("3.  食品工業")
    print("4.  塑膠工業")
    print("5.  紡織纖維")
    print("6.  電機機械")
    print("7.  電器電纜")
    print("8.  化學生技醫療")
    print("9.  化學工業")
    print("10. 生技醫療業")
    print("11. 玻璃陶瓷")
    print("12. 造紙工業")
    print("13. 鋼鐵工業")
    print("14. 橡膠工業")
    print("15. 汽車工業")
    print("16. 電子工業")
    print("17. 半導體業")
    print("18. 電腦及週邊設備業")
    print("19. 光電業")
    print("20. 通信網路業")
    print("21. 電子零組件業")
    print("22. 電子通路業")
    print("23. 資訊服務業")
    print("24. 其他電子業")
    print("25. 建材營造")
    print("26. 航運業")
    print("27. 觀光事業")
    print("28. 金融保險")
    print("29. 貿易百貨")
    print("30. 油電燃氣業")
    print("31. 綜合")
    print("32. 其他")
    # let user choose their desired value
    while True:
        color_output("white", "Enter tse_stock class:", False)
        ans=input("")
        if ans.isdigit()==False: # not a only digit input, show error
            color_output("red", "[ERROR] contains non-digit symbol\n", True)
        elif int(ans)>32 or int(ans)<1: # only 32 options can be choosed
            color_output("red", "[ERROR] index exceeds limitation\n", True)
        else:# start assign return value(including fullname & type_code)
            match int(ans):
                case 1:
                    return ["tse全部", "ALL"]
                case 2:
                    return ["水泥工業", "01"]
                case 3:
                    return ["食品工業", "02"]
                case 4:
                    return ["塑膠工業", "03"]
                case 5:
                    return ["紡織纖維", "04"]
                case 6:
                    return ["電機機械", "05"]
                case 7:
                    return ["電器電纜", "06"]
                case 8:
                    return ["化學生技醫療", "07"]
                case 9:
                    return ["化學工業", "21"]
                case 10:
                    return ["生技醫療業", "22"]
                case 11:
                    return ["玻璃陶瓷", "08"]
                case 12:
                    return ["造紙工業", "09"]
                case 13:
                    return ["鋼鐵工業", "10"]
                case 14:
                    return ["橡膠工業", "11"]
                case 15:
                    return ["汽車工業", "12"]
                case 16:
                    return ["電子全部", "13"]
                case 17:
                    return ["半導體業", "24"]
                case 18:
                    return ["電腦及週邊設備業", "25"]
                case 19:
                    return ["光電業", "26"]
                case 20:
                    return ["通信網路業", "27"]
                case 21:
                    return ["電子零組件業", "28"]
                case 22:
                    return ["電子通路業", "29"]
                case 23:
                    return ["資訊服務業", "30"]
                case 24:
                    return ["其他電子業", "31"]
                case 25:
                    return ["建材營造", "14"]
                case 26:
                    return ["航運業", "15"]
                case 27:
                    return ["觀光事業", "16"]
                case 28:
                    return ["金融保險", "17"]
                case 29:
                    return ["貿易百貨", "18"]
                case 30:
                    return ["油電燃氣業", "23"]
                case 31:
                    return ["綜合", "19"]
                case 32:
                    return ["其他", "20"]
        

# get different class of otc
def class_of_otc():
    from output import color_output
    # print out all different class of otc
    print("1.  otc全部")
    print("2.  食品工業")
    print("3.  塑膠工業")
    print("4.  紡織纖維")
    print("5.  電機機械")
    print("6.  電器電纜")
    print("7.  化學工業")
    print("8.  玻璃陶瓷")
    print("9.  鋼鐵工業")
    print("10. 橡膠工業")
    print("11. 建材營造")
    print("12. 航運業")
    print("13. 觀光事業")
    print("14. 金融業")
    print("15. 貿易百貨")
    print("16. 其他")
    print("17. 生技醫療類")
    print("18. 油電燃氣類")
    print("19. 半導體類")
    print("20. 電腦及週邊類")
    print("21. 光電業類")
    print("22. 通信網路類")
    print("23. 電子零組件類")
    print("24. 電子通路類")
    print("25. 資訊服務類")
    print("26. 其他電子類")
    print("27. 文化創意業")
    print("28. 農業科技業")
    print("29. 電子商務業")
    print("30. 電子全部")
    # let user choose their desired value
    while True:
            color_output("white", "Enter otc_stock class:", False)
            ans=input("")
            if ans.isdigit()==False: # not a only digit input, show error
                color_output("red", "[ERROR] contains non-digit symbol\n", True)
            elif int(ans)>30 or int(ans)<1: # only 29 options can be choosed
                color_output("red", "[ERROR] index exceeds limitation\n", True)
            else:
                # start assign return value(including fullname & type_code.)
                match int(ans):
                    case 1:
                        return ["otc全部", "AL"]
                    case 2:
                        return ["食品工業", "02"]
                    case 3:
                        return ["塑膠工業", "03"]
                    case 4:
                        return ["紡織纖維", "04"]
                    case 5:
                        return ["電機機械", "05"]
                    case 6:
                        return ["電器電纜", "06"]
                    case 7:
                        return ["化學工業", "21"]
                    case 8:
                        return ["玻璃陶瓷", "08"]
                    case 9:
                        return ["鋼鐵工業", "10"]
                    case 10:
                        return ["橡膠工業", "11"]
                    case 11:
                        return ["建材營造", "14"]
                    case 12:
                        return ["航運業", "15"]
                    case 13:
                        return ["觀光事業", "16"]
                    case 14:
                        return ["金融業", "17"]
                    case 15:
                        return ["貿易百貨", "18"]
                    case 16:
                        return ["其他", "20"]
                    case 17:
                        return ["生技醫療類", "22"]
                    case 18:
                        return ["油電燃氣類", "23"]
                    case 19:
                        return ["半導體類", "24"]
                    case 20:
                        return ["電腦及週邊類", "25"]
                    case 21:
                        return ["光電業類", "26"]
                    case 22:
                        return ["通信網路類", "27"]
                    case 23:
                        return ["電子零組件類", "28"]
                    case 24:
                        return ["電子通路類", "29"]
                    case 25:
                        return ["資訊服務類", "30"]
                    case 26:
                        return ["其他電子類", "31"]
                    case 27:
                        return ["文化創意業", "32"]
                    case 28:
                        return ["農業科技業", "33"]
                    case 29:
                        return ["電子商務業", "34"]
                    case 30:
                        return ["電子全部", "all_elecs"]

# this function will decide if the result output with stock_class
def yes_or_no(info):
    from output import color_output
    while True:
        color_output("white", info, False)
        ans=input()
        if ans.lower()=='y':
            return True
        elif ans.lower()=='n':
            return False
        else:
            color_output("red", "[ERROR] Only (Y)es or (N)o\n", True)

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
            result=data[idx].strip('\n').strip('][').split(', ')
            return_data.append(result)
    ff.close()
    return return_data

# --------------------------Analyze Mathod and Functions------------------------------
# since OTC official website do not provide "電子全部" stocks data json file
# so, collect one by one, and find stockid list by ourselves
def all_elecs_otc_stockid_list():
    stockid_result=[] # used to store valid analyzed stockid 
    # the following is ALL 'type_code' needed to collect (CAN BE MODIFIED or CHANGED)
    # since the collection list is too long, so only print out 
    # "電子全部 of OTC" instead of "半導體 of OTC" "電子商務 of OTC".... for siplification
    # [半導體類, 電腦及週邊類, 光電業類, 通信網路類, 電子零組件類, 電子通路類, 資訊服務類, 其他電子類, 電子商務業]
    type_code=["24", "25", "26", "27", "28", "29", "30", "31", "34"] # type code contains all 電子類 class type_code
    from output import color_output
    color_output("purple", "Request", False)
    color_output("yellow", "電子全部 of OTC", False)
    color_output("purple", "data", False)
    # generate random timstamp for url
    from datetime import datetime
    from urllib import request
    import os, json
    # get each class of stockid, then parse and store result to stockid_result
    for code in type_code:
        curr_t = datetime.now()
        time_stamp = datetime.timestamp(curr_t)
        URL="https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&d=&se="+str(code)+"&_="+str(time_stamp*1000)
        request.urlretrieve(URL, "[tpex].json")
        # find all valid data from the [tpex].json
        with open("[tpex].json", 'r') as ff:
            data=json.loads(ff.read())
            for stock in data['aaData']:
                if len(stock[0])==4:
                    if int(stock[0])>1000:
                        stockid_result.append(str(stock[0]))
    # finally, sort the stockid_result list from smallest to largest
    stockid_result.sort()
    os.remove("[tpex].json")
    color_output("green", "[PASS]", True)
    return stockid_result

# get analyzed stock id list of tse or otc, and use it to read content of the json file 
# finally, remove the file, keep directory clean
def specified_class_stockid_list(stock_type, stock_class):
    if stock_type=="tse":
        filename="[twse].json"
        if stock_class=="ALL": # stock_class decides the keyWord used in json file
            keyWord='data9'
        else:
            keyWord='data1'
    else:
        filename="[tpex].json"
        keyWord='aaData'
    # open the json file and find all stockid of specific stock class
    stockid_result=[] # used to store valid analyzed stockid 
    with open(filename, 'r') as ff:
        import json, os
        data=json.loads(ff.read())
        # get all valid stockid from keyWord(TSE:'data1'; OTC:'aaData)
        for stock in data[keyWord]:
            # store all valid stock id for given class to stockid_result
            if len(stock[0])==4: # remove those id too long stock(often contains alphabet)
                if int(stock[0])>1000: # remove those stock id too small(ex. 0050, 0051...)
                    stockid_result.append(str(stock[0]))
        os.remove(filename)
        return stockid_result

# get slope which analyze either High or Low price of two consectutive weeks
# used to find out if a reversed-point happened or not
def slope(newdata, olddata):
    if float(newdata)-float(olddata)>0:
        return 1
    elif float(newdata)-float(olddata)==0:
        return 0
    else: # slope<0 case
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

# get week data of specific stockid in given weekdata list
# if no match stock data, then return "NaN"
def specific_stockid_data(weekdata, stockid):
    for stock in weekdata:
        if str(stock[0])==str(stockid): # matched stock id, then return the data list
            return stock
        else:
            continue
    return "NaN"

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

# this function helps stock_class_of_result to find matched id and class
def pair_matched_id_class(stockid_list, class_data):
    # used to save final result
    final_result=[];
    # run through all elements in stockid_list
    for stockid in stockid_list:
        for item in class_data:
            # find matched, append to final_result
            if str(item["id"])==str(stockid):
                # special case for stock_class undefined
                stock_class="";
                if item["class"]=="":
                    stock_class="未定義"
                else:
                    stock_class=item["class"]
                data={"id":str(stockid), "class":str(stock_class)}
                final_result.append(data)
                break
            # last one, but still not find the corresponding stock id 
            elif item==class_data[len(class_data)-1]:
                data={"id":str(stockid), "class":"未找到相符代號"}
            else:
                continue
    return final_result

# this function will get the stock_class for the passed stocks
# input: a list that has all passed stocks id
def stock_class_of_result(stockid_list):
    from output import color_output
    id_str=""
    color_output("purple", "Request", False)
    color_output("yellow", "stock class", False)
    color_output("purple", "info", False)
    # run through all stock id, and save them in a string seperated with comma
    for stockid in stockid_list:
        id_str=id_str+stockid;
        if stockid!=stockid_list[len(stockid_list)-1]:
            id_str=id_str+","
    URL="https://isin.twse.com.tw/isin/single_main.jsp?owncode="+id_str+"&stockname="
    import requests
    from bs4 import BeautifulSoup
    # use HTTP GET method and html parser to parse result
    response=requests.get(URL)
    if response.status_code==200:
        # parse the HTML content, decode in MS950, a.k.a. Big-5
        soup=BeautifulSoup(response.content.decode("MS950"), "html.parser")
        table_element=soup.find("table", class_="h4")
        # find the table_element(data stored in table format)
        if table_element:
            rows=table_element.find_all("tr")[1:]
            # iterate over rows to get the table data
            # cells[2]: stockid
            # cells[6]: stock class
            class_data=[]
            for row in rows:
                cells=row.find_all("td")
                mapped_data={"id":cells[2].get_text(), "class":cells[6].get_text()}
                class_data.append(mapped_data)
            color_output("green", "[PASS]", True)
        else:
            color_output("red", "[FAIL] -> failed to parse the table", True)
    else:
        color_output("red", "[FAIL] -> response status not 200", True)
    # called the other function to find matched id and class
    # and save the final result to a map list
    color_output("purple", "Parsing", False)
    color_output("yellow", "stock class", False)
    color_output("purple", "info", False)
    final_result=pair_matched_id_class(stockid_list, class_data) 
    color_output("green", "[PASS]", True)
    return final_result
