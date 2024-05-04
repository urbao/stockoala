'''
stock_scraper: collect TWSE and TPEX daily data, and combine to weekly, and monthly data
'''

from output import color_out
from urllib import request
from datetime import datetime
import json
import os


# (return True: has data needed to prune/ False: Nvm)
# TWSE Case
# use urllib module to retrieve TWSE specific day's data(including code/name/open/high/low/close)
# date: used to specified certain date data
# type_code: used to append on URL for requesting correct data
# stock_type: used to show info when collecting specific class stock data
def twse(date, type_code, stock_type):
    color_out("purple", "獲取", False)
    if date!="":
        color_out("yellow", str(date)+" TWSE", False)
    else:
        color_out("yellow", str(stock_type)+" of TSE", False)
    color_out("purple", "資料", False)
    URL="https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date="+str(date)+"&type="+str(type_code)
    request.urlretrieve(URL, str(date)+"[twse].json")
    # check if files is no data
    with open(str(date)+"[twse].json", 'r', encoding="utf-8") as j:
        content=json.loads(j.read())
        if(content['stat']=="很抱歉，沒有符合條件的資料!"): # no data stored
            color_out("red", "[失敗]", True)
            os.remove(date+"[twse].json")
            return False
        elif(content['stat']=="查詢日期大於今日，請重新查詢!"): # no data stored
            color_out("red", "[失敗]", True)
            os.remove(date+"[twse].json")
            return False
        else:
            color_out("green", "[成功]", True)
            # success: prune the corresponding date json file
            if date!="":
                twse_prune(date)
            return True
        

# TPEX Case
def tpex(date, type_code, stock_type):
    color_out("purple", "獲取", False)
    if date!="":
        color_out("cyan", str(date)+" TPEX", False)
    else:
        color_out("cyan", str(stock_type)+" OTC", False)
    color_out("purple", "資料", False)
    # generate random timstamp for url
    curr_t = datetime.now()
    time_stamp = datetime.timestamp(curr_t)
    # find current date for url(based on url date format)
    if date!="":
        search_date=str(int(date[0:4])-1911)+"/"+date[4:6]+"/"+date[6:8]
    else:
        search_date="" # when parsing data, no date spcefied
    URL="https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&d="+str(search_date)+"&se="+str(type_code)+"&_="+str(time_stamp*1000)
    request.urlretrieve(URL, str(date)+"[tpex].json")
    # check if files is no data
    with open(str(date)+"[tpex].json", 'r', encoding="utf-8") as j:
        content=json.loads(j.read())
        if(content['iTotalRecords']==0): # no data stored
            color_out("red", "[失敗]", True)
            os.remove(date+"[tpex].json")
            return False
        else:
            color_out("green", "[成功]", True)
            if date!="":
                tpex_prune(date)
            return True
        
# prune data action only keeps the ID|HIGH|LOW|OPEN|CLOSE|TRANSACTION in original json file
# the following two functions are used at `twse` and `tpex`, respectively
def twse_prune(date):
    with open(date+"[twse].json", 'r', encoding="utf-8") as j:
        import json
        alldata=json.loads(j.read())
        f=open(date+"[twse].txt",'w', encoding="utf-8")
        # only left the `data9` related stocks' data
        data=alldata['data9']
        for idx in range(len(data)):
            if len(data[idx][0])==4: # prune those whose id is longer than 4 digit
                if int(data[idx][0])>1000: # prune those whose
                    Id=str(data[idx][0])
                    Transaction=str(int(int(data[idx][2].replace(',', ''))/1000)) # use trade share to calc trade count
                    Open=str(data[idx][5])
                    High=str(data[idx][6])
                    Low=str(data[idx][7])
                    Close=str(data[idx][8])
                    line="["+Id+", "+High+", "+Low+", "+Open+", "+Close+", "+Transaction+", tse]"
                    f.write(line+"\n")
        f.close()
    j.close()
    os.remove(date+"[twse].json")
    return

def tpex_prune(date):
    with open(str(date)+"[tpex].json", 'r', encoding="utf-8") as j:
        import json
        alldata=json.loads(j.read())
        f=open(str(date)+"[tpex].txt",'w', encoding="utf-8")
        data=alldata['aaData']
        for idx in range(int(alldata['iTotalRecords'])):
            if len(data[idx][0])<5:
                Id=str(data[idx][0])
                Transaction=str(int(int(data[idx][7].replace(',', ''))/1000)) # use trade share to calc trade count
                Open=str(data[idx][4])
                High=str(data[idx][5])
                Low=str(data[idx][6])
                Close=str(data[idx][2])
                line="["+Id+", "+High+", "+Low+", "+Open+", "+Close+", "+Transaction+", otc]"
                f.write(line+"\n")
        f.close()
    j.close()
    os.remove(str(date)+"[tpex].json")
    return