'''
config: read the config.json file and read user-input configurement
'''
from output import color_out
from datetime import datetime, date

# get the data stored within config.json
def get_config_file_content():
    import json
    with open('config.json', 'r') as f:
        config_data=json.load(f)
    return config_data

# get valid start date input from user(should be MONDAY)
def user_defined_start_date():
    # show reminder first
    color_out("cyan", "-- 日期格式: 20220320 and 20011009", True)
    color_out("cyan", "-- 持續天數: 5 and 6", True)
    color_out("red", "-- [失敗] 代表該天資料不存在\n",True)
    while(True):
        color_out("white", "輸入日期:", False)
        ans=input("")
        if(len(ans)!=8): # date too long or short
            color_out("red", "[錯誤] 不允許的日期格式\n", True)
            continue
        try: # error when trying convert to date object
            datetime.strptime(ans, '%Y%m%d')
        except ValueError:
            color_out("red", "[錯誤] 不允許的日期格式\n", True)
            continue
        # check if it's Monday
        if(date(int(ans[0:4]), int(ans[4:6]), int(ans[6:8])).weekday()==0):
            return ans
        else:
            color_out("red", "[錯誤] 不是星期一的日期\n", True)
            continue

# get user desired data collect period length in day unit
def user_defined_period_length():
    while(True):
        color_out("white", "輸入持續天數:", False)
        period=input("")
        if period.isdigit(): # check if only digit(NO negative sign or others allowed)
            if int(period)>0: # period can not be 0 days
                return period
            else:
                color_out("red", "[錯誤] 持續天數不可為0天\n", True)
        else:
            color_out("red", "[錯誤] 輸入只能是整數\n", True)

# get date based on given timedelta
# if delta negative, then the date will be past
# if delta positive, then the date will be future
def date_with_given_delta(date, delta):
    from datetime import datetime
    from datetime import timedelta
    curr_date=datetime.strptime(date, '%Y%m%d')
    result=str(curr_date+timedelta(int(delta)))
    year=str(result[0:4])
    month=str(result[5:7])
    day=str(result[8:10])
    return year+month+day

# get TSE_INDEX or OTC_INDEX by user manually
def index_from_user(type):
    color_out("white", "輸入 "+str(type)+" 指數(%):", False)
    ans=input("")
    try:
        ans=float(ans)
        return ans
    except:
        color_out("red", "[錯誤] 只允許小數點輸入\n", True)

# get specific type of stocks needed to analyze
def tse_or_otc():
    while True:
        color_out("white", "輸入股票類型(1.tse/2.otc):", False)
        ans=input("")
        if ans.isdigit()==True:
            if int(ans)==1:
                return "tse"
            elif int(ans)==2:
                return "otc"
            else:
                color_out("red", "[錯誤] 只能輸入1或2\n", True)
        else:
            color_out("red", "[錯誤] 輸入只能是整數\n", True)

# get the analyzed class of tse
def class_of_tse():
    # print out all different class of tse
    print("1.  tse全部")
    print("2.  水泥工業")
    print("3.  食品工業")
    print("4.  塑膠工業")
    print("5.  紡織纖維")
    print("6.  電機機械")
    print("7.  電器電纜")
    print("8.  化學生技醫療")
    print("9.  化學工業")
    print("10. 生技醫療業")
    print("11. 玻璃陶瓷")
    print("12. 造紙工業")
    print("13. 鋼鐵工業")
    print("14. 橡膠工業")
    print("15. 汽車工業")
    print("16. 電子工業")
    print("17. 半導體業")
    print("18. 電腦及週邊設備業")
    print("19. 光電業")
    print("20. 通信網路業")
    print("21. 電子零組件業")
    print("22. 電子通路業")
    print("23. 資訊服務業")
    print("24. 其他電子業")
    print("25. 建材營造")
    print("26. 航運業")
    print("27. 觀光事業")
    print("28. 金融保險")
    print("29. 貿易百貨")
    print("30. 油電燃氣業")
    print("31. 綜合")
    print("32. 其他")
    # let user choose their desired value
    while True:
        color_out("white", "輸入tse類股類型:", False)
        ans=input("")
        if ans.isdigit()==False: # not a only digit input, show error
            color_out("red", "[錯誤] 輸入只能是整數\n", True)
        elif int(ans)>32 or int(ans)<1: # only 32 options can be choosed
            color_out("red", "[錯誤] 該數字沒有對應的類股類型\n", True)
        else:# start assign return value(including fullname & type_code)
            match int(ans):
                case 1:
                    return ["tse全部", "ALL"]
                case 2:
                    return ["水泥工業", "01"]
                case 3:
                    return ["食品工業", "02"]
                case 4:
                    return ["塑膠工業", "03"]
                case 5:
                    return ["紡織纖維", "04"]
                case 6:
                    return ["電機機械", "05"]
                case 7:
                    return ["電器電纜", "06"]
                case 8:
                    return ["化學生技醫療", "07"]
                case 9:
                    return ["化學工業", "21"]
                case 10:
                    return ["生技醫療業", "22"]
                case 11:
                    return ["玻璃陶瓷", "08"]
                case 12:
                    return ["造紙工業", "09"]
                case 13:
                    return ["鋼鐵工業", "10"]
                case 14:
                    return ["橡膠工業", "11"]
                case 15:
                    return ["汽車工業", "12"]
                case 16:
                    return ["電子全部", "13"]
                case 17:
                    return ["半導體業", "24"]
                case 18:
                    return ["電腦及週邊設備業", "25"]
                case 19:
                    return ["光電業", "26"]
                case 20:
                    return ["通信網路業", "27"]
                case 21:
                    return ["電子零組件業", "28"]
                case 22:
                    return ["電子通路業", "29"]
                case 23:
                    return ["資訊服務業", "30"]
                case 24:
                    return ["其他電子業", "31"]
                case 25:
                    return ["建材營造", "14"]
                case 26:
                    return ["航運業", "15"]
                case 27:
                    return ["觀光事業", "16"]
                case 28:
                    return ["金融保險", "17"]
                case 29:
                    return ["貿易百貨", "18"]
                case 30:
                    return ["油電燃氣業", "23"]
                case 31:
                    return ["綜合", "19"]
                case 32:
                    return ["其他", "20"]
                
# get the analyzed class of otc
def class_of_otc():
    # print out all different class of otc
    print("1.  otc全部")
    print("2.  食品工業")
    print("3.  塑膠工業")
    print("4.  紡織纖維")
    print("5.  電機機械")
    print("6.  電器電纜")
    print("7.  化學工業")
    print("8.  玻璃陶瓷")
    print("9.  鋼鐵工業")
    print("10. 橡膠工業")
    print("11. 建材營造")
    print("12. 航運業")
    print("13. 觀光事業")
    print("14. 金融業")
    print("15. 貿易百貨")
    print("16. 其他")
    print("17. 生技醫療類")
    print("18. 油電燃氣類")
    print("19. 半導體類")
    print("20. 電腦及週邊類")
    print("21. 光電業類")
    print("22. 通信網路類")
    print("23. 電子零組件類")
    print("24. 電子通路類")
    print("25. 資訊服務類")
    print("26. 其他電子類")
    print("27. 文化創意業")
    print("28. 農業科技業")
    print("29. 電子商務業")
    print("30. 電子全部")
    # let user choose their desired value
    while True:
            color_out("white", "輸入otc類股類型:", False)
            ans=input("")
            if ans.isdigit()==False: # not a only digit input, show error:
                color_out("red", "[錯誤] 輸入只能是整數\n", True)
            elif int(ans)>30 or int(ans)<1: # only 29 options can be choosed
                color_out("red", "[錯誤] 該數字沒有對應的類股類型\n", True)
            else:
                # start assign return value(including fullname & type_code.)
                match int(ans):
                    case 1:
                        return ["otc全部", "AL"]
                    case 2:
                        return ["食品工業", "02"]
                    case 3:
                        return ["塑膠工業", "03"]
                    case 4:
                        return ["紡織纖維", "04"]
                    case 5:
                        return ["電機機械", "05"]
                    case 6:
                        return ["電器電纜", "06"]
                    case 7:
                        return ["化學工業", "21"]
                    case 8:
                        return ["玻璃陶瓷", "08"]
                    case 9:
                        return ["鋼鐵工業", "10"]
                    case 10:
                        return ["橡膠工業", "11"]
                    case 11:
                        return ["建材營造", "14"]
                    case 12:
                        return ["航運業", "15"]
                    case 13:
                        return ["觀光事業", "16"]
                    case 14:
                        return ["金融業", "17"]
                    case 15:
                        return ["貿易百貨", "18"]
                    case 16:
                        return ["其他", "20"]
                    case 17:
                        return ["生技醫療類", "22"]
                    case 18:
                        return ["油電燃氣類", "23"]
                    case 19:
                        return ["半導體類", "24"]
                    case 20:
                        return ["電腦及週邊類", "25"]
                    case 21:
                        return ["光電業類", "26"]
                    case 22:
                        return ["通信網路類", "27"]
                    case 23:
                        return ["電子零組件類", "28"]
                    case 24:
                        return ["電子通路類", "29"]
                    case 25:
                        return ["資訊服務類", "30"]
                    case 26:
                        return ["其他電子類", "31"]
                    case 27:
                        return ["文化創意業", "32"]
                    case 28:
                        return ["農業科技業", "33"]
                    case 29:
                        return ["電子商務業", "34"]
                    case 30:
                        return ["電子全部", "all_elecs"]
