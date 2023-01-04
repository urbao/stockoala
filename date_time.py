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
    color_output("cyan", "-- Period Example(days): 5 and 6", True)
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

# get usr desired stock data collected period length
def get_period_length():
    while(True):
        color_output("white", "Enter Period:", False)
        period=input("")
        if(period.isdigit()): # check if only digit(NO negative sign or others allowed)
            if(int(period)>0): # period can not be 0 days
                return period
            else:
                color_output("red", "[ERROR] Period can NOT be 0 day\n", True)
        else:
            color_output("red", "[ERROR] contains non-digit symbol\n", True)
