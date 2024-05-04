'''
collect: used other modules to collect TSE and OTC data
'''
from output import color_out
from time import sleep
import stock_scraper
import data_combiner
import config

# get the start date and period length from user
start_date=str(config.user_defined_start_date())
period_len=int(config.user_defined_period_length())

# use iterations to collect data from Monday to given period length
date=start_date
period_data_list=[] # this is used to save data from day 1 to day n
color_out("cyan", "\n==============$$$$===============", True)
for i in range(period_len): # THE 5 CAN CHANGED TO ANY LENGTH OF DAYS AS WE WANT
    # twse and tpex will reteieve and pre-process data
    tse_success=stock_scraper.twse(date, "ALL", "ALL_TSE")
    sleep(2)
    otc_success=stock_scraper.tpex(date, "AL", "ALL_OTC")
    sleep(2)
    # append the single-day-data-list to period_data_list if any file is collected successfuly
    if tse_success==True or otc_success==True:
        period_data_list.append(data_combiner.merge_same_day_data(date)) 
    date=str(config.date_with_given_delta(date, 1)) # add 1 day, continue collect next date stock data

print("\n")
color_out("purple", "抓取股票代號列表", False)
stockid_list=data_combiner.stockid_list(period_data_list)
color_out("green", "[完成]", True)
color_out("purple", "整合為週線資料", False)
data_combiner.generate_weekly_report(period_data_list, stockid_list, start_date)
color_out("green", "[完成]", True)
print("\n")
# final show reminder and some info
color_out("purple", "股票總數:", False)
color_out("green", str(len(stockid_list)), True)
color_out("cyan", "==============$$$$===============", True)