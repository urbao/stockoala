'''
Analyze Method: from thisweek and traceback to past.
If the move "reverse-point" occurs in this week, which means there must exist a valley point
in the past few week, and another peak point much long ago than valley point .So, try to use the slope of HIGH and LOW data to analyze
'''

#---Receive system parameter first---#
import sys
LANG=sys.argv[1]
SYS=sys.argv[2]
DIRPATH=sys.argv[3]

import get, os, output
#-------Path Definition(DO NOT MODIFY)------------#
# datapath: used to get data list for analyzing

datapath="path_to_data_directory"
if SYS=="Linux":
    datapath=DIRPATH+"data/"
else:
    datapath=DIRPATH+"data\\"

#-------------------------------------------------#
# get reverse-sorted filename_list
# So, the first filename is the latest one
filename_list=get.filename_list(datapath)

# initialize a list array, and stored recent 5 weeks data based on 
# filename_list into weekdata_list
max_track_weeks=5

# check if data not enough, exit and print out warning
if len(filename_list)<max_track_weeks:
    if LANG=="EN":
        output.color_output("red", "[ERROR] stock data is NOT enough(at least "+str(max_track_weeks)+" weeks)", True)
    else:
        output.color_output("red", "[錯誤] 股票周線資料不足(至少 "+str(max_track_weeks)+" 周)", True)
    import sys
    sys.exit()

#-----------------------------------analyze starting--------------------------------------#
# first, let user choose the type they want to analyze(tse or otc)
stock_type=get.tse_or_otc(LANG)

# secondly, let user decide the class of stocks they want to analyze
# stock_class receive: ["NAME OF TYPE", "TYPE_CODE_REPLACED_WITH_URL"]
# example: ["電子全部", "13"]
stock_class=[]
if stock_type=="tse":
    stock_class=get.class_of_tse(LANG)
else:
    stock_class=get.class_of_otc(LANG)
if SYS=="Linux":
    os.system("clear") # clear the whole screen
else:
    os.system("cls")

# third, get the analyzed_stock id list(if the class is all_tse|all_otc|all_elecs,
# then no need for asking stock website, instead, use the datafile to find stockidlist)
# TSE PART
if stock_type=="tse":
    success=get.twse("", str(stock_class[1]), str(stock_class[0]), LANG)
    if success==False: # check if the desired analyzed class is empty or not
        if LANG=="EN":
            output.color_output("red", "[ERROR] "+str(stock_class[0])+" class of tse is empty", True)
        else:
            output.color_output("red", "[錯誤] "+str(stock_class[0])+" tse類股沒有任何對應的股票", True)
        os.remove("[twse].json")
        import sys
        sys.exit() # no further analyze required
    else:
        parsed_stockid_list=get.specified_class_stockid_list("tse", stock_class[1])
# OTC PART
else:
    if stock_class[1]=="all_elecs": 
        # special case(need to collect all_elecs by ourselves, and all collected classes can be modified in get.py)
        parsed_stockid_list=get.all_elecs_otc_stockid_list(LANG)
    else:
        success=get.tpex("", str(stock_class[1]), str(stock_class[0]), LANG)
        if success==False:# check if the desired analyzed class is empty or not
            if LANG=="EN":
                output.color_output("red", "[ERROR] "+str(stock_class[0])+" class of otc is empty", True)
            else:
                output.color_output("red", "[錯誤] "+str(stock_class[0])+" otc類股沒有任何對應的股票", True)
            os.remove("[tpex].json")
            import sys
            sys.exit() # no further analyze required
        else:
            parsed_stockid_list=get.specified_class_stockid_list("otc", stock_class[1])
# print out some parsed_stockid_list & total_count for confimation
if LANG=="EN":
    output.color_output("purple", "Total Count:", False)
    output.color_output("yellow", str(len(parsed_stockid_list)), False)
    output.color_output("purple", "(ex.", False)
else:
    output.color_output("purple", "總共數量:", False)
    output.color_output("yellow", str(len(parsed_stockid_list)), False)
    output.color_output("purple", "(ex.", False)
# print out top three, if total count is less than 3, print all
counter=0
for idx in range(len(parsed_stockid_list)):
    if counter==3:
        break
    else:
        output.color_output("yellow", str(parsed_stockid_list[idx])+",", False)
    counter+=1
output.color_output("onlybackspace", "\b\b", False) # remove extra ',' in the line
output.color_output("purple", "...)", True)

# fourth part, start analyzing
# collect last 5 weeks data, and store them in weekdata_list
weekdata_list=[] # store all stockdata for past 5 weeks, and later use parsed_stockid_list to analyze
os.chdir(datapath) # move to data dir for reading files
for i in range(max_track_weeks):
    weekdata_list.append(get.file_data(filename_list[i]))
# weekdata_list[0]: this week data[LATEST]
# weekdata_list[1]: one week data
# weekdata_list[2]: two week data
# weekdata_list[3]: three week data
# weekdata_list[4]: four week data

# fifth part, analyze the stock in parsed_stockid_list, and store result to result[]
# also, write the result to result.txt
result=[]
# ---------- DISABLE PRICE CHANGE OPTIONS ------------ #
# 1. Limitation: the stock's change is belowed the INDEX should NOT be considered
#INDEX=-1.0
#if stock_type=="tse":
#    INDEX=get.index_from_user('TSE', LANG)
#else:
#    INDEX=get.index_from_user('OTC', LANG)

import json
config_file=DIRPATH+"config.json"
with open(config_file, 'r') as json_file:
    data=json.load(json_file)
# 2. Limitation: stock weekly transaction which is below 500 should NOT be considered
min_trans_toleration=data["min_trans_toleration"]

# 3. Limitation: stock lowest price is higher than $350 should NOT be considered
max_stock_price=data["max_stock_price"]


# all analyze should only consider those on the list of parsed_stockid_list
for stockid in parsed_stockid_list:
    # Get THISWEEK_DATA of the current stockid(will be used later)
    stockid_thisweek_data=get.specific_stockid_data(weekdata_list[0], stockid)
    # ----- First, Use THISWEEK_DATA [existance] to remove some stocks
    # If exist: keep analyzing, else: continue to next stock
    if stockid_thisweek_data=="NaN":
        continue
    # ---- Second, Use THISWEEK_DATA [transaction] to prune more stocks
    # If below min_trans_toleration: continue to next stock, else: keep analyzing
    elif int(stockid_thisweek_data[5])<min_trans_toleration:
        continue
    # ---- Third, Use THISWEEK_DATA [price_change] to prune more stocks
    # If TSE(OTC) stock is below TSE(OTC) INDEX:continue to next stock, else: keep analyzing
    #elif int(get.stock_price_change(weekdata_list, stockid))<INDEX:
    #    continue
    # ---- Fourth, Use THISWEEK_DATA [lowest_price] to prune more stocks
    # If lowest_price is higher than max_stock_price(too expensive):continure to next stock, else: keep analyzing
    elif float(stockid_thisweek_data[2])>max_stock_price:
        continue
    # ---- Finally, Use Reverse-Point to find out the result
    # If pass, then print out result and write it into result.txt
    else:
        # reset data(d) to empty list(purpose: store all pass five weeks valid data)
        d=[]
        # append corresponding stock this week and valid 1,2,3,4 weeks ago data to a 2D list
        # so the data will all be valid, and consecutive(much easier for analyzing)
        d=get.conti_valid_stock_data(weekdata_list, stockid)
        # 2. check if the valid data is enough to create a reverse-point
        # at least the valid data need three weeks, plus one stock id, so the length of 'd' should be larger than 4
        # valid_week_count is represented how many valid weeks data stored in the 'd' list
        valid_week_count=len(d)-1
        if valid_week_count<3:
            #output.color_output("cyan", stock[0]+": I gave up", True)
            continue
        else:
            from get import slope      
            # Start analyzing process
            # d[0]: stock id
            # d[1]: this week high/low price
            # two possible condition of 1st part: 2 or 3 data reach valley point
            # two possible condition of 2nd part, too(HOWEVER, need to consider IF THE VALID DATA IS ENOUGH, some might only have 3 or 4 datas)
            # 1. 2 data reach valley point(BOTH high/low has pos slope)
            if slope(d[1][0],d[2][0])==1 and slope(d[1][1], d[2][1])==1:
                # 3 weeks reverse finished
                if slope(d[2][0],d[3][0])==-1 and slope(d[2][1],d[3][1])==-1:
                    result.append(str(stockid))
                    continue
                # 4 weeks reverse finished(NEED TO CHECK VALID DATA COUNT ENOUGH OR NOT)
                # check if data has 4 weeks
                if valid_week_count>=4:
                    if slope(d[2][0], d[4][0])==-1 and slope(d[2][1], d[4][1])==-1 and slope(d[2][0], d[3][0])>=0 and slope(d[2][1],d[3][1])<=0:
                        result.append(str(stockid))
                        continue
            # 2. 3 data reach valley point(d[2] is convered within d[3] boundary)
            # Covered: the d[2] high is -le than d[3] high, and d[2] low is -ge than d[3] low 
            if slope(d[1][0], d[3][0])==1 and slope(d[1][1], d[3][1])==1 and slope(d[2][0], d[3][0])<=0 and slope(d[2][1],d[3][1])>=0:
                # 4 weeks to reverse
                if valid_week_count>=4:
                    if slope(d[3][0], d[4][0])==-1 and slope(d[3][1], d[4][1])==-1:
                        result.append(str(stockid))
                        continue
                # 5 weeks to reverse
                if valid_week_count==5:
                    if slope(d[3][0], d[5][0])==-1 and slope(d[3][1], d[5][1])==-1 and slope(d[3][0], d[4][0])>=0 and slope(d[3][1],d[4][1])<=0:
                        result.append(str(stockid))
                        continue
            # 3. valid_week_count==5: the 2,3,4 weeks data has one covered the other two weeks data also should be counted
            # Case1: week2 cover week3 & week4
            # Case2: week3 cover week2 & week4(ALREADY TAKEN INTO CONSDER 5 LINES ABOVE)
            # Case3: week4 cover week2 & week3
            # the following will consider Case1 & Case3
            if valid_week_count==5:
                #Case1
                if slope(d[1][0],d[2][0])==1 and slope(d[1][1],d[2][1])==1 and slope(d[2][0],d[5][0])==-1 and slope(d[2][1],d[5][1])==-1:
                    if slope(d[2][0],d[3][0])>=0 and slope(d[2][0],d[4][0])>=0 and slope(d[2][1],d[3][1])<=0 and slope(d[2][1],d[4][1])<=0:
                        result.append(str(stockid))
                        continue
                #Case3
                if slope(d[1][0],d[4][0])==1 and slope(d[1][1],d[4][1])==1 and slope(d[4][0],d[5][0])==-1 and slope(d[4][1],d[5][1])==-1:
                    if slope(d[2][0],d[4][0])<=0 and slope(d[3][0],d[4][0])<=0 and slope(d[2][1],d[4][1])>=0 and slope(d[3][1],d[4][1])>=0:
                        result.append(str(stockid))
                        continue
                
#-----------------------------------analyze finished--------------------------------------#
# print out result and some info
from datetime import datetime
if LANG=="EN":
    output.color_output("purple", "\nTime:", False)
    output.color_output("white", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True)
    output.color_output("purple", "Type:", False)
    output.color_output("white", stock_type+"-"+stock_class[0], True)
else:
    output.color_output("purple", "\n時間:", False)
    output.color_output("white", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True)
    output.color_output("purple", "股票類型:", False)
    output.color_output("white", stock_type+"-"+stock_class[0], True)

index=1
counter=1
for stock in result:
    if index%2==1:
        output.color_output("yellow", str(stock), False)
    else:
        output.color_output("cyan", str(stock), False)
    # check if newline or not
    if counter%20==0:
        output.color_output("newline", "", True)
        index+=1
    else:
        output.color_output("space", " ", False)
    counter+=1
if LANG=="EN":
    output.color_output("purple", "\nPass Total Count:", False)
    output.color_output("green", str(len(result)), False)
    output.color_output("yellow", "("+str(round(float(len(result))*100/float(len(parsed_stockid_list)), 2))+"%)", True)
else:
    output.color_output("purple", "\n通過總共數量:", False)
    output.color_output("green", str(len(result)), False)
    output.color_output("yellow", "("+str(round(float(len(result))*100/float(len(parsed_stockid_list)), 2))+"%)", True)
