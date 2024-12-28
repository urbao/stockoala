'''
monthly_analyze: analyze data with monthly-strategy, also before analyzing, update the monthly-report file
'''

from output import color_out
import os
import json


def update_lowest_low(monthly_price_dict, id_val, low_val):
    # consider the case that low_val is '----'
    if low_val=='--' or low_val=='----':
        return

    # if id_val existed in dict, then choose the lowest low_val
    if id_val in monthly_price_dict:
        monthly_price_dict[id_val]['low'] = min(monthly_price_dict[id_val]['low'], float(low_val))
    # otherwise, append it to dict and init other high/open/close price at the same time 
    # (because the update_lowest_low is called at first, no need to do this at the rest of update monthly price functions)
    else:
        monthly_price_dict[id_val] = {'low': float(low_val), 'high': None, 'open': None, 'close': None}

def update_highest_high(monthly_price_dict, id_val, high_val):
    if high_val=='--' or high_val=='----':
        return
    
    # if id_val existed in dict, then choose the highest high_val
    if id_val in monthly_price_dict and monthly_price_dict[id_val]['high'] != None:
        monthly_price_dict[id_val]['high'] = max(monthly_price_dict[id_val]['high'], float(high_val));
    # otherwise, append it to dict and init other high/open/close price at the same time
    else:
        monthly_price_dict[id_val]['high'] = float(high_val)

def update_monthly_open(monthly_price_dict, id_val, open_val):
    if open_val=='--' or open_val == '----':
        return
    
    # check if the monthly_price_dict open for that specific id is still null
    if id_val in monthly_price_dict and monthly_price_dict[id_val]['open'] == None:
        monthly_price_dict[id_val]['open'] = open_val
    # if the open is already not null, meaning the open data is no needed to be updated
    else:
        return
    
def update_monthly_close(monthly_price_dict, id_val, close_val):
    if close_val=='--' or close_val=='----':
        return

    # no matter what, just keep update the close_val
    # reason: the file is loaded ascending in date, so if we keep update
    # , and we'll get the last day close_val
    if id_val in monthly_price_dict:
        monthly_price_dict[id_val]['close'] = close_val
        return

# update specific month's monthly report
def update_specific_month_report(path, monthly_report):
    # first save all the files content into an dict
    monthly_price_dict={}
    # we sort the filename in Ascending mode, so we can know the open and close price of that month
    for filename in sorted(os.listdir(str(path))):
        filepath=os.path.join(path, filename)
        if os.path.isfile(filepath) and filename.endswith('.txt'):
            with open(filepath, 'r') as file:
                for line in file:
                    data = line.replace('\'','').replace('[','').replace(']','').split(',')
                    id_val = data[0].strip()  # Assuming 'Id' is the first value
                    high_val = data[1].strip()
                    low_val = data[2].strip()  # Assuming 'low' is the third value
                    open_val = data[3].strip()
                    close_val = data[4].strip()
                    
                    # calling the function to update the monthly price data
                    update_lowest_low(monthly_price_dict, id_val, low_val)
                    update_highest_high(monthly_price_dict, id_val, high_val)
                    update_monthly_open(monthly_price_dict, id_val, open_val)
                    update_monthly_close(monthly_price_dict, id_val, close_val)

    # save the updated month report(Id and low_val) to a file
    # format: json, get the low_val more quickly
    with open(os.path.join(path, monthly_report+".json"), 'w') as json_file:
        json.dump(monthly_price_dict, json_file)
    return
        

# chooese the latest 3 months data, and update the monthly report
# return type: the latest 3 months' monthly report path
def update_monthly_report(monthly_path):
    folder_list=os.listdir(str(monthly_path))
    path_list=[]
    # sort the folder_list, so we can choose the latest 3 months folder
    folder_list = sorted(folder_list, reverse=True)
    # only need to update the latest 3 months folder 
    for folder in folder_list[:3]:
        color_out("purple", "更新", False)
        color_out("yellow", str(folder), False)
        color_out("purple", "月線資料", False)
        path=os.path.join(monthly_path, str(folder))
        path_list.append(path) # append the path to list for monthly_strategy_analysis usage
        update_specific_month_report(path, folder)
        color_out("green", "[成功]", True)
    return path_list


def monthly_strategy_analysis(path_list, weekly_analysis_result):
    this_month={}
    one_month_ago={}
    two_month_ago={}
    final_result=[]
    # path_list is already in orientation of latest-first sorted
    for idx in range(3):
        json_filename=path_list[idx][-6:]
        with open(os.path.join(path_list[idx], json_filename+'.json'), 'r') as json_file:
            if idx==0:
                this_month=json.load(json_file)
            elif idx==1:
                one_month_ago=json.load(json_file)
            else:
                two_month_ago=json.load(json_file)
    
    # start monthly strategy analysis
    '''
    Step 1: run through all stocks in weekly_analysis_result, there's no need for checking those stocks which not passed the weekly_analysis
    Step 2: check if the stock fits the monthly-strategy

    Monthly-Strategy (2 conditions)
        - case 1: this_month low_val < one_month_ago low_val
        - case 2: one_month_ago low_val < two_month_ago low_val
        - case 3: this_month low_val(high_val) > one_month_ago low_val(high_val)
                                                +
                  one_month_ago low_val(high_val) > two_month_ago low_val(high_val)
                                                +
                  this_month open > this_month close
    '''

    for stockid in weekly_analysis_result:
        # case 1
        if stockid in this_month and stockid in one_month_ago:
            if this_month[stockid]['low']<one_month_ago[stockid]['low']:
                final_result.append(stockid)
                continue
        # case 2
        if stockid in one_month_ago and stockid in two_month_ago:
            if one_month_ago[stockid]['low']<two_month_ago[stockid]['low']:
                final_result.append(stockid)
                continue
        # case 3
        if stockid in one_month_ago and stockid in two_month_ago:
            if this_month[stockid]['low'] > one_month_ago[stockid]['low'] and this_month[stockid]['high'] > one_month_ago[stockid]['high']:
                if one_month_ago[stockid]['low'] > two_month_ago[stockid]['low'] and one_month_ago[stockid]['high'] > two_month_ago[stockid]['high']:
                    if this_month[stockid]['open'] > this_month[stockid]['close']:
                        final_result.append(stockid)
                        continue
    return final_result
    
