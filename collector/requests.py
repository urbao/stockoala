from output import color_output

# check if date is valid
def val_date(chk_date):
    from datetime import datetime, date
    if(len(chk_date)!=8): # date too long or short
        color_output("red", "[ERROR] Invalid Format\n", True)
        return False
    try: # error when trying convert to date object
        dateObj=datetime.strptime(chk_date, '%Y%m%d')
    except ValueError:
        color_output("red", "[ERROR] Invalid Date\n", True)
        return False
    # check if it's Monday
    if(date(int(chk_date[0:4]), int(chk_date[4:6]), int(chk_date[6:8])).weekday()==0):
        return True
    else:
        color_output("red", "[ERROR] Not Monday\n", True)
        return False

# get start date input from user         
def get_date():
    # show reminder
    color_output("cyan", "-- Date Example: 20220320 and 20011009", True)
    color_output("cyan", "-- Reminder: Auto collect data of five days", True)
    color_output("red", "-- [FAIL] means data NOT collected or parsed\n",True)
    while(True):
        color_output("white", "Enter Date:", False)
        date=input("")
        if(val_date(date)):
            return date
            
# add up one day
def add_1day(date):
    from datetime import datetime
    from datetime import timedelta
    curr_date=datetime.strptime(date, '%Y%m%d')
    next_date=str(curr_date+timedelta(days=1))
    year=str(next_date[0:4])
    month=str(next_date[5:7])
    day=str(next_date[8:10])
    return year+month+day

# use urllib module to retrieve TWSE specific day's data(including code/name/open/high/low/close)
def twse(date):
    color_output("purple", "Request", False)
    color_output("yellow", date+" TWSE", False)
    color_output("purple", "data", False)
    from urllib import request
    content=request.urlretrieve("https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date="+date+"&type=ALL", date+"[twse].csv")
    # check if the file is empty, and print status
    import os
    if os.stat(date+"[twse].csv").st_size == 0:# empty file(show warning)
        color_output("red", "[FAIL]", True)
        return
    else:
        color_output("green", "[PASS]", True)
        return

def tpex(date):
    color_output("purple", "Request", False)
    color_output("cyan", date+" TPEX", False)
    color_output("purple", "data", False)
    # generate random timstamp for url
    from datetime import datetime
    curr_t = datetime.now()
    time_stamp = datetime.timestamp(curr_t)
    # find current date for url(based on url date format)
    from urllib import request
    serch_date=str(int(date[0:4])-1911)+"/"+date[4:6]+"/"+date[6:8]
    request.urlretrieve("https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&d="+serch_date+"&se=AL&_="+str(time_stamp*1000), date+"[tpex].json")
    with open(date+"[tpex].json", 'r') as j:
        import json
        content=json.loads(j.read())
        if(content['iTotalRecords']==0): # no data stored
            color_output("red", "[FAIL]", True)
            return
        else:
            color_output("green", "[PASS]", True)
            return
