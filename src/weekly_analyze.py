'''
weekly_analyze: analyze stock data with weekly strategy, and return the result
'''

import config
import analyze_helper

CONFIG=config.get_config_file_content()

def weekly_strategy_analysis(weekdata_list, analyzed_stockid_list):
    result=[]
    # ---------- DISABLE PRICE CHANGE OPTIONS ------------ #
    # 1. Limitation: the stock's change is belowed the INDEX should NOT be considered
    #INDEX=-1.0
    #if stock_type=="tse":
    #    INDEX=config.index_from_user('TSE')
    #else:
    #    INDEX=config.index_from_user('OTC')
    # all analyze should only consider those on the list of analyzed_stokid_list
    for stockid in analyzed_stockid_list:
        # Get THISWEEK_DATA of the current stockid(will be used later)
        stockid_thisweek_data=analyze_helper.specific_stockid_data(weekdata_list[0], stockid)
        # ----- First, Use THISWEEK_DATA [existance] to remove some stocks
        # If exist: keep analyzing, else: continue to next stock
        if stockid_thisweek_data=="NaN":
            continue
        # ---- Second, Use THISWEEK_DATA [transaction] to prune more stocks
        # If below min_trans_toleration: continue to next stock, else: keep analyzing
        # elif int(stockid_thisweek_data[5])<CONFIG['min_trans_toleration']:
        #     continue
        # ---- Third, Use THISWEEK_DATA [price_change] to prune more stocks
        # If TSE(OTC) stock is below TSE(OTC) INDEX:continue to next stock, else: keep analyzing
        #elif int(get.stock_price_change(weekdata_list, stockid))<INDEX:
        #    continue
        # ---- Fourth, Use THISWEEK_DATA [lowest_price] to prune more stocks
        # If lowest_price is higher than max_stock_price(too expensive):continure to next stock, else: keep analyzing
        # elif float(stockid_thisweek_data[2])>CONFIG['max_stock_price']:
        #     continue
        # ---- Finally, Use Reverse-Point to find out the result
        # If pass, then print out result and write it into result.txt
        else:
            # reset data(d) to empty list(purpose: store all pass five weeks valid data)
            d=[]
            # append corresponding stock this week and valid 1,2,3,4 weeks ago data to a 2D list
            # so the data will all be valid, and consecutive(much easier for analyzing)
            d=analyze_helper.conti_valid_stock_data(weekdata_list, stockid)
            # 2. check if the valid data is enough to create a reverse-point
            # at least the valid data need three weeks, plus one stock id, so the length of 'd' should be larger than 4
            # valid_week_count is represented how many valid weeks data stored in the 'd' list
            valid_week_count=len(d)-1
            if valid_week_count<3:
                #output.color_output("cyan", stock[0]+": I gave up", True)
                continue
            else:
                from analyze_helper import slope  
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
                # 4. valid_week_count==6: the 2,3,4,5 weeks data has ibe civered the ither three weejs data
                # Case 1: week 2 cover week 3,4,5
                # Case 2: week 3 cover week 2,4,5
                # Case 3: week 4 cover week 2,3,5
                # Case 4: week 5 cover week 2,3,4
                if valid_week_count==6:
                    # Case 1
                    if slope(d[1][0],d[2][0])==1 and slope(d[1][1],d[2][1])==1 and slope(d[2][0],d[6][0])==-1 and slope(d[2][1],d[6][1])==-1:
                        if slope(d[2][0],d[3][0])>=0 and slope(d[2][0],d[4][0])>=0 and slope(d[2][0],d[5][0])>=0:
                            if slope(d[2][1],d[3][1])<=0 and slope(d[2][1],d[4][1])<=0 and slope(d[2][1],d[5][1])<=0:
                                result.append(str(stockid))
                                continue
                    # Case 2
                    if slope(d[1][0],d[3][0])==1 and slope(d[1][1],d[3][1])==1 and slope(d[3][0],d[6][0])==-1 and slope(d[3][1],d[6][1])==-1:
                        if slope(d[3][0],d[2][0])>=0 and slope(d[3][0],d[4][0])>=0 and slope(d[3][0],d[5][0])>=0:
                            if slope(d[3][1],d[2][1])<=0 and slope(d[3][1],d[4][1])<=0 and slope(d[3][1],d[5][1])<=0:
                                result.append(str(stockid))
                                continue
                    # Case 3
                    if slope(d[1][0],d[4][0])==1 and slope(d[1][1],d[4][1])==1 and slope(d[4][0],d[6][0])==-1 and slope(d[4][1],d[6][1])==-1:
                        if slope(d[4][0],d[2][0])>=0 and slope(d[4][0],d[3][0])>=0 and slope(d[4][0],d[5][0])>=0:
                            if slope(d[4][1],d[2][1])<=0 and slope(d[4][1],d[3][1])<=0 and slope(d[4][1],d[5][1])<=0:
                                result.append(str(stockid))
                                continue
                    # Case 4
                    if slope(d[1][0],d[5][0])==1 and slope(d[1][1],d[5][1])==1 and slope(d[5][0],d[6][0])==-1 and slope(d[5][1],d[6][1])==-1:
                        if slope(d[5][0],d[2][0])>=0 and slope(d[5][0],d[3][0])>=0 and slope(d[5][0],d[4][0])>=0:
                            if slope(d[5][1],d[2][1])<=0 and slope(d[5][1],d[3][1])<=0 and slope(d[5][1],d[4][1])<=0:
                                result.append(str(stockid))
                                continue

    return result # result contains those stocks pass the weekly strategy analysis