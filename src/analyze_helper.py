'''
analyze_helper: contains some funtions needed in analyze progress
'''

from output import color_out
import os
import sys
import stock_scraper

# get the data filelist in reverse order, so the latest will be the first file
def filename_list(filepath):
    filelist=os.listdir(str(filepath))
    filelist.sort(reverse=True)
    # run through all filename, and remove unwanted analyzed filename from the filelist
    for file in filelist:
        if(file==".git/"):
            filelist.remove(".git/")
        if(file=="README.md"):
            filelist.remove("README.md")
    return filelist

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
    with open(filename, 'r', encoding="utf-8") as ff:
        import json
        data=json.loads(ff.read())
        # get all valid stockid from keyWord(TSE:'data1'; OTC:'aaData)
        for stock in data[keyWord]:
            # store all valid stock id for given class to stockid_result
            if len(stock[0])==4: # remove those id too long stock(often contains alphabet)
                if int(stock[0])>1000: # remove those stock id too small(ex. 0050, 0051...)
                    stockid_result.append(str(stock[0]))
    os.remove(filename)
    return stockid_result

# since OTC official website do not provide "電子全部" stocks data json file
# so, collect one by one, and find stockid list by ourselves
def all_elecs_otc_stockid_list():
    stockid_result=[] # used to store valid analyzed stockid 
    # the following is ALL 'type_code' needed to collect (CAN BE MODIFIED or CHANGED)
    # since the collection list is too long, so only print out 
    # "電子全部 of OTC" instead of "半導體 of OTC" "電子商務 of OTC".... for siplification
    # [半導體類, 電腦及週邊類, 光電業類, 通信網路類, 電子零組件類, 電子通路類, 資訊服務類, 其他電子類, 電子商務業]
    type_code=["24", "25", "26", "27", "28", "29", "30", "31", "34"] # type code contains all 電子類 class type_code
    color_out("purple", "獲取", False)
    color_out("yellow", "電子全部 of OTC", False)
    color_out("purple", "資料", False)
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
        with open("[tpex].json", 'r', encoding="utf-8") as ff:
            data=json.loads(ff.read())
            for stock in data['aaData']:
                if len(stock[0])==4:
                    if int(stock[0])>1000:
                        stockid_result.append(str(stock[0]))
    # finally, sort the stockid_result list from smallest to largest
    stockid_result.sort()
    os.remove("[tpex].json")
    color_out("green", "[成功]", True)
    return stockid_result


# get the analyzed stock id list of this week
def analyzed_stockid_list(stock_class, stock_type):
    # TSE PART
    if stock_type=="tse":
        success=stock_scraper.twse("", str(stock_class[1]), str(stock_class[0]))
        if success==False: # check if the desired analyzed class is empty or not
            color_out("red", "[錯誤] "+str(stock_class[0])+" tse類股沒有任何對應的股票", True)
            os.remove("[twse].json")
            sys.exit() # no further analyze required
        else:
            analyzed_stockid_list=specified_class_stockid_list("tse", stock_class[1])
    # OTC PART
    else:
        if stock_class[1]=="all_elecs": 
            # special case(need to collect all_elecs by ourselves, and all collected classes can be modified in get.py)
            analyzed_stockid_list=all_elecs_otc_stockid_list()
        else:
            success=stock_scraper.tpex("", str(stock_class[1]), str(stock_class[0]))
            if success==False:# check if the desired analyzed class is empty or not
                color_out("red", "[錯誤] "+str(stock_class[0])+" otc類股沒有任何對應的股票", True)
                os.remove("[tpex].json")
                sys.exit() # no further analyze required
            else:
                analyzed_stockid_list=specified_class_stockid_list("otc", stock_class[1])
    # print out the info
    color_out("purple", "總共數量:", False)
    color_out("yellow", str(len(analyzed_stockid_list)), False)
    color_out("purple", "(ex.", False)
    # print out top three, if total count is less than 3, print all
    counter=0
    for idx in range(len(analyzed_stockid_list)):
        if counter==3:
            break
        else:
            color_out("yellow", str(analyzed_stockid_list[idx])+",", False)
        counter+=1
    color_out("onlybackspace", "\b\b", False) # remove extra ',' in the line
    color_out("purple", "...)", True)
    return analyzed_stockid_list


# try to read data of given filename, and return as a list datatype
def file_data(filename):
    return_data=[]
    with open(str(filename), 'r', encoding="utf-8") as ff:
        data=ff.readlines()
        for idx in range(len(data)):
            result=data[idx].strip('\n').strip('][').split(', ')
            return_data.append(result)
    ff.close()
    return return_data


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