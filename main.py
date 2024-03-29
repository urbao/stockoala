# This script will control the current workflow based on user preference
# user can either [select op code] or [type op command]
# valid op list below:
# 1. collect weekly stockdata
# 2. parse weekly data 
# 3. show all stock data files
# 4. clear the screen
# 5. exit the program

### Global Variables ###
LANG="EN"
SYS="Linux"
USERNAME="koala"
DIRPATH="$HOME"

from src.output import color_output

# load variables
# return True: success
# return False: failed
def load_var():
    try:
        with open(".config", 'r') as file:
            for line in file:
                title, content=line.strip().split('=') 
                if title=="LANG":
                    global LANG
                    LANG=content
                elif title=="SYS":
                    global SYS
                    SYS=content
                elif title=="USERNAME":
                    global USERNAME
                    USERNAME=content
                elif title=="DIRPATH":
                    global DIRPATH
                    DIRPATH=content
                else:
                    color_output("red", "ERROR: an extra unknown line {"+title+":"+content+"}", True)
                    return False
    except FileNotFoundError:
        color_output("red", "ERROR: config file not exist, try run again setup file", True)
        return False
    if LANG=="EN":
        color_output("white", "type 'help' or '?' to show valid commands\n", True)
    else:
        color_output("white", "輸入 'help' 或 '?' 顯示所有可執行的指令\n", True)
    return True

# collect weekly stockdata
def collect_data():
    import subprocess
    if SYS=="Linux":
        subprocess.call(['python3', 'src/collect.py', LANG])
    else:
        subprocess.call(['python', 'src\\collect.py', LANG])
    # after the collecing action, put the data file into data directory
    import glob, os
    file_list=glob.glob("20*.txt")
    for file in file_list:
        if SYS=="Linux":
            os.replace(file, "data/"+file)
        else:
            os.replace(file, "data\\"+file)
    return

# parse weekly data
def parse_data():
    import subprocess
    if SYS=="Linux":
        subprocess.call(['python3', 'src/parse.py', LANG, SYS, DIRPATH])
    else:
        subprocess.call(['python', 'src\\parse.py', LANG, SYS, DIRPATH])
    return

# show all stock data files
def show_files():
    from src.get import filename_list
    if SYS=="Linux":
        dataPath=DIRPATH+"data/"
    else:
        dataPath=DIRPATH+"data\\"
    if LANG=="EN":
        color_output("cyan", "---------- File List ----------", True)
    else:
        color_output("cyan", "---------- 檔案 列表 ----------", True)
    # filename_list returns filelist in descent order
    idx=0;
    for file in reversed(filename_list(dataPath)):
        color_output("yellow", str(idx+1)+".", False)
        if idx%2==0:
            color_output("white", str(file), False)
        else:
            color_output("white", str(file), True)
        idx+=1
    if idx%2==1:
        print("")
    color_output("cyan", "-------------------------------", True)
    return

# clear the screen
def clear_screen(SYS):
    import os
    if SYS=="Linux":
        os.system('clear')
    else:
        os.system('cls')
    return

# show the help msg
def show_helpMsg(LANG):
    if LANG=="EN":
        color_output("green", "    code/cmd  response action", True)
        color_output("white", "   1/collect  collect weekly stockdata", True)
        color_output("white", "   2/parse    parse recent 5 weeks stockdata", True)
        color_output("white", "   3/show     show all existed stockdata files", True)
        color_output("white", "   4/clear    clear the screen", True)
        color_output("white", "   5/exit     exit the program", True)
    else:
        color_output("green", "   代號/指令  預期效果", True)
        color_output("white", "   1/collect  蒐集每周資料", True)
        color_output("white", "   2/parse    分析過去五周資料", True)
        color_output("white", "   3/show     顯示現有資料檔案", True)
        color_output("white", "   4/clear    清空現在畫面", True)
        color_output("white", "   5/exit     離開程式", True)
    return

# main function
def main():
    # update the global variables
    # check anything is good or not
    if load_var()==False:
        import time
        time.sleep(3)
        return

    while True:
        color_output("purple", USERNAME+":", False)
        ans=input()
        if ans=="1" or ans=="collect":
            collect_data()
        elif ans=="2" or ans=="parse":
            parse_data()
        elif ans=="3" or ans=="show":
            show_files()
        elif ans=="4" or ans=="clear":
            clear_screen(SYS)
        elif ans=="5" or ans=="exit":
            break
        elif ans=="help" or ans=="?":
            show_helpMsg(LANG)
        else:
            if LANG=="EN":
                color_output("red", "ERROR: No corresponding action", True)
            else:
                color_output("red", "ERROR: 沒有相對應的指令", True)
    return

if __name__=="__main__":
    main()
