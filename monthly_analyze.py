'''
monthly_analyze: analyze data with monthly-strategy, also before analyzing, update the monthly-report file
'''

from output import color_out
import os
import json


def update_lowest_low(low_price_dict, id_val, low_val):
    # consider the case that low_val is '----'
    if low_val=='--' or low_val=='----':
        return

    # if id_val existed in dic, then choose the lowest low_val
    if id_val in low_price_dict:
        low_price_dict[id_val] = min(low_price_dict[id_val], float(low_val))
    # otherwise, append it to dict
    else:
        low_price_dict[id_val] = float(low_val)

# update specific month's monthly report
def update_specific_month_report(path, monthly_report):
    # first save all the files content into an dict
    low_price_dict={}
    for filename in os.listdir(str(path)):
        filepath=os.path.join(path, filename)
        if os.path.isfile(filepath) and filename.endswith('.txt'):
            with open(filepath, 'r') as file:
                for line in file:
                    data = line.replace('\'','').replace('[','').replace(']','').split(',')
                    id_val = data[0].strip()  # Assuming 'Id' is the first value
                    low_val = data[2].strip()  # Assuming 'low' is the third value
                    update_lowest_low(low_price_dict, id_val, low_val)

    # save the updated month report(Id and low_val) to a file
    # format: json, get the low_val more quickly
    with open(os.path.join(path, monthly_report+".json"), 'w') as json_file:
        json.dump(low_price_dict, json_file)
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
    '''

    for stockid in weekly_analysis_result:
        # case 1
        if stockid in this_month and stockid in one_month_ago:
            if this_month[stockid]<one_month_ago[stockid]:
                final_result.append(stockid)
                continue
        # case 2
        if stockid in one_month_ago and stockid in two_month_ago:
            if one_month_ago[stockid]<two_month_ago[stockid]:
                final_result.append(stockid)
                continue
    return final_result
    
