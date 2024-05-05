'''
data_combiner: merge same day data, and generate weekly-report data 
'''
import os
import config
CONFIG=config.get_config_file_content()

# combine TWSE and TPEX data of the same date into one file named with date
def merge_same_day_data(date):
    stock_data=[]
    with open(str(date)+"[twse].txt", 'r', encoding="utf-8") as twse:
        twse_data=twse.readlines()
        for idx in range(len(twse_data)):
            twse_result=twse_data[idx].strip('\n').strip('][').split(', ')
            stock_data.append(twse_result)
    twse.close()
    with open(str(date)+"[tpex].txt", 'r', encoding="utf-8") as tpex:
        tpex_data=tpex.readlines()
        for idx in range(len(tpex_data)):
            tpex_result=tpex_data[idx].strip('\n').strip('][').split(', ')
            stock_data.append(tpex_result)
    tpex.close()
    # sort the stock_data by the stock id,
    # and return the result as a 2D-list
    stock_data=sorted(stock_data, key=lambda l: l[0])

    # save the daily data into monthly-data directory
    # check if the path is exised before saving data
    monthly_path=os.path.join(CONFIG['monthly_path'], str(date)[:-2])
    if not os.path.exists(monthly_path):
        os.makedirs(monthly_path)
    
    # start saving data
    with open(os.path.join(monthly_path, str(date)+'.txt'), 'w', encoding='utf-8') as file:
        for row in stock_data:
            file.write(str(row)+'\n')

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
# save the weekly-report to weekly-data directory
def generate_weekly_report(period_data_list, stockid_list, start_date):    
    with open(CONFIG['weekly_path']+str(start_date)+'.txt', 'w', encoding="utf-8") as file:
        for idx in range(len(stockid_list)):
            Id=str(stockid_list[idx])
            High=str(stock_period_max_min(period_data_list, Id, 'Max'))
            Low=str(stock_period_max_min(period_data_list, Id, 'min'))
            Open=str(stock_period_open(period_data_list, Id))
            Close=str(stock_period_close(period_data_list, Id))
            Transaction=str(stock_period_transaction(period_data_list, Id))
            Type=str(stock_period_type(period_data_list, Id))
            line="["+Id+", "+High+", "+Low+", "+Open+", "+Close+", "+Transaction+", "+Type+"]\n"
            file.write(line)
    file.close()
    return