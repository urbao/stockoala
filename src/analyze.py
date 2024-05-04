'''
analyze: used the weekly-data and monthly-data to analyze current week stocks

method: (default: both used(allowed to modify in config.json))
    - weekly-data: check if the data has a `reverse-point` using slope concept
    - monthly-data: check the if the low point is lower than last month
'''
import os
import sys
import config
import analyze_helper
from output import color_out
import weekly_analyze
import monthly_analyze
from datetime import datetime

CONFIG=config.get_config_file_content()

# get the reverse-sorted weekly-data filename list
filename_list=analyze_helper.filename_list(CONFIG['weekly_path'])
# consider the weely data not enough to analyze
if len(filename_list)<CONFIG['max_analyzed_weeks']:
    color_out("red", "[錯誤] 股票周線資料不足(至少 "+str(CONFIG['max_analyzed_weeks'])+" 周)", True)
    sys.exit()

# first, let user choose the type they want to analyze(tse or otc)
stock_type=config.tse_or_otc()

# secondly, let user decide the class of stocks they want to analyze
# stock_class receive: ["NAME OF TYPE", "TYPE_CODE_REPLACED_WITH_URL"]
# example: ["電子全部", "13"]
stock_class=[]
if stock_type=="tse":
    stock_class=config.class_of_tse()
else:
    stock_class=config.class_of_otc()
if CONFIG['system']=="Linux":
    os.system("clear") # clear the whole screen
else:
    os.system("cls")

# third, get the analyzed_stock id list(if the class is all_tse|all_otc|all_elecs,
analyzed_stockid_list=analyze_helper.analyzed_stockid_list(stock_class, stock_type)

# fourth part, start analyzing
# collect last 6 weeks data, and store them in weekdata_list
weekdata_list=[] # store all stockdata for past 6 weeks, and later use analyzed_stokid_list to analyze
os.chdir(CONFIG['weekly_path']) # move to data dir for reading files
for i in range(CONFIG['max_analyzed_weeks']):
    weekdata_list.append(analyze_helper.file_data(filename_list[i]))
# weekdata_list[0]: this week data[LATEST]
# weekdata_list[1]: one week data
# weekdata_list[2]: two week data
# weekdata_list[3]: three week data
# weekdata_list[4]: four week data
# weekdata_list[5]: five week data

# fifth part, analyze the stock in analyzed_stockid_list using weekly_strategy, and store result to result[]
weekly_analysis_result=weekly_analyze.weekly_strategy_analysis(weekdata_list, analyzed_stockid_list)

# sixth part, go to monthly-data folder, and update the month file
# path_list is the latest 3 months' folder's path
path_list=monthly_analyze.update_monthly_report(CONFIG['monthly_path'])

# sixth part, analyze the stock in weekly_analysis_result using monthly_strategy
final_analysis_result=monthly_analyze.monthly_strategy_analysis(path_list, weekly_analysis_result)

# final part, print out the final_analysis_result
color_out("purple", "\n時間:", False)
color_out("white", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True)
color_out("purple", "股票類型:", False)
color_out("white", stock_type+"-"+stock_class[0], True)
index=1
counter=1
for stock in final_analysis_result:
    if index%2==1:
        color_out("yellow", str(stock), False)
    else:
        color_out("cyan", str(stock), False)
    # check if newline or not
    if counter%20==0:
        color_out("newline", "", True)
        index+=1
    else:
        color_out("space", " ", False)
    counter+=1
color_out("purple", "\n通過總共數量:", False)
color_out("green", str(len(final_analysis_result)), False)
color_out("yellow", "("+str(round(float(len(final_analysis_result))*100/float(len(analyzed_stockid_list)), 2))+"%)", True)
