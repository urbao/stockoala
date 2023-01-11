'''
Analyze Method: from thisweek and traceback to past.
If the move "reverse-point" occurs in this week, which means there must exist a valley point
in the past few week, and another peak point much long ago than valley point .So, try to use the slope of HIGH and LOW data to analyze
'''
import numpy as np
import get, os
#-------Path Definition(DO NOT MODIFY)------------#
# dirpath: used to store result file
# datapath: used to get data list for analyzing

datapath="/home/eason/Desktop/stockoala/data/"

#-------------------------------------------------#

# get reverse-sorted filename_list
# So, the first filename is the latest one
filename_list=get.filename_list(datapath)

# initialize a list array, and stored recent 5 weeks data based on 
# filename_list into weekdata_list
max_track_weeks=5
weekdata_list=[]
os.chdir(datapath) # move to data dir for reading files
for i in range(max_track_weeks):
    weekdata_list.append(get.file_data(filename_list[i]))
# weekdata_list[0]: this week data[LATEST]
# weekdata_list[1]: one week data
# weekdata_list[2]: two week data
# weekdata_list[3]: three week data
# weekdata_list[4]: four week data
'''
Analyze Result Symbol Explanation:
1. Get history data up to 5 weeks ago 
2. Find out all stockid which has reversed-point within last 5 weeks

Analyze Method:
1. For all stocks, we collect the latest 5 weeks data
2. Then pass the data to function of get.py for analyzing
3. print out result

Possible situation:
1. The week has no data --> just ignore this stock
2. The data is too rare(ex: --/----/NaN), so no enough data to recognize --> ignore this stock
3. week has enough data --> analyze 3,4,5 weeks reverse or not
'''
#-----------------------------------analyze starting--------------------------------------#
# consider every stock in this week data
# each time, find the stock 5 week data, and store in list
# pass to function for analyzing

# first get the TWSE and TPEX INDEX of the week from the user
# 1. Limitation: the stock's change is belowed the min(TWSE_INDEX, TPEX_INDEX) should NOT be considered
TWSE_INDEX=get.index_from_user('TWSE')
TPEX_INDEX=get.index_from_user('TPEX')

# 2. Limitation: stock weekly transaction which is below 500 should NOT be considered
min_trans_toleration=500

# used to store analyze result
result=[]
# all analyze should only consider those on the list of weekdata_list[0](this week)
for stock in weekdata_list[0]:
    ##################################FIRST PART USE TRANSACTION TO PRUNE MORE STOCKS#######################################
    if int(stock[5])<min_trans_toleration: # transaction less than 500, so ignore this stock
        print(stock[0]+": smaller than 500("+str(stock[5])+")")
        continue
    ############################### SECOND PART USE CHANGE V.S. INDEX TO PRUNE MORE STOCKS ################################# 
    elif get.stock_price_change(weekdata_list, stock[0])<min(TWSE_INDEX, TPEX_INDEX): # the change of stock is smller than min of INDEX
        print(stock[0]+": too small change("+str(get.stock_price_change(weekdata_list, stock[0]))+"%)")
        continue
    #################################THIRD PART USE REVERSE-POINT TO PRUNE SOME STOCKS######################################
    # check if this stock has data of this week
    # if NOT, then no need for keep going
    elif stock[1]=="NaN":
        print(stock[0]+": no valid price")
        continue
    # if the stock has data of this week, then analyze it
    else:
        # reset data(d) to empty list(purpose: store all pass five weeks valid data)
        d=[]
        # append corresponding stock this week and valid 1,2,3,4 weeks ago data to a 2D list
        # so the data will all be valid, and consecutive(much easier for analyzing)
        d=get.conti_valid_stock_data(weekdata_list, stock[0])
        # 2. check if the valid data is enough to create a reverse-point
        # at least the valid data need three weeks, plus one stock id, so the length of 'd' should be larger than 4
        # valid_week_count is represented how many valid weeks data stored in the 'd' list
        valid_week_count=len(d)-1
        if valid_week_count<3:
            print(stock[0]+": not enough week data")
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
                    result.append(str(d[0]))
                # 4 weeks reverse finished(NEED TO CHECK VALID DATA COUNT ENOUGH OR NOT)
                # check if data has 4 weeks
                if valid_week_count>=4:
                    if slope(d[2][0], d[4][0])==-1 and slope(d[2][1], d[4][1])==-1 and slope(d[2][0], d[3][0])>=0 and slope(d[2][1],d[3][1])<=0:
                        result.append(str(d[0]))
            # 2. 3 data reach valley point(d[2] is convered within d[3] boundary)
            # Covered: the d[2] high is -le than d[3] high, and d[2] low is -ge than d[3] low 
            if slope(d[1][0], d[3][0])==1 and slope(d[1][1], d[3][1])==1 and slope(d[2][0], d[3][0])<=0 and slope(d[2][1],d[3][1])>=0:
                # 4 weeks to reverse
                if valid_week_count>=4:
                    if slope(d[3][0], d[4][0])==-1 and slope(d[3][1], d[4][1])==-1:
                        result.append(str(d[0]))
                # 5 weeks to reverse
                if valid_week_count==5:
                    if slope(d[3][0], d[5][0])==-1 and slope(d[3][1], d[5][1])==-1 and slope(d[3][0], d[4][0])>=0 and slope(d[3][1],d[4][1])<=0:
                        result.append(str(d[0]))
      
                        
#-----------------------------------analyze finished--------------------------------------#
for i in range(len(result)):
    print(result[i])
print("Count: "+str(len(result)))