from color import color_output

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
