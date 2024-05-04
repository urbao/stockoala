# This script will control the current workflow based on user preference
# user can either [select op code] or [type op command]
# valid op list below:
# 1. collect weekly stockdata
# 2. parse weekly data 
# 3. show all stock data files
# 4. clear the screen
# 5. exit the program

from output import color_out
import config
import os
import subprocess


CONFIG=config.get_config_file_content()

def show_helpMsg():
    color_out("green", "   代號/指令  預期效果", True)
    color_out("white", "   1/collect  蒐集每周資料", True)
    color_out("white", "   2/parse    分析過去五周資料", True)
    color_out("white", "   3/show     顯示現有資料檔案", True)
    color_out("white", "   4/clear    清空現在畫面", True)
    color_out("white", "   5/exit     離開程式", True)
    return

def collect_data():
    if CONFIG['system']=='Linux':
        subprocess.call(['python3', 'collect.py'])
    else:
        subprocess.call(['python', 'collect.py'])
    return

def parse_data():
    if CONFIG['system']=='Linux':
        subprocess.call(['python3', 'analyze.py'])
    else:        
        subprocess.call(['python', 'analyze.py'])
    return

def show_files():
    from analyze_helper import filename_list
    color_out("cyan", "---------- 檔案 列表 ----------", True)
    # filename_list returns filelist in descent order
    idx=0;
    for file in reversed(filename_list(CONFIG['weekly_path'])):
        color_out("yellow", str(idx+1)+".", False)
        if idx%2==0:
            color_out("white", str(file), False)
        else:
            color_out("white", str(file), True)
        idx+=1
    if idx%2==1:
        print("")
    color_out("cyan", "-------------------------------", True)
    return

def clear_screen():
    if CONFIG['system']=="Linux":
        os.system('clear')
    else:
        os.system('cls')
    return

def main():
    while True:
        color_out("purple", CONFIG['username']+":", False)
        ans=input()
        if ans=="1" or ans=="collect":
            collect_data()
        elif ans=="2" or ans=="parse":
            parse_data()
        elif ans=="3" or ans=="show":
            show_files()
        elif ans=="4" or ans=="clear":
            clear_screen()
        elif ans=="5" or ans=="exit":
            break
        elif ans=="help" or ans=="?":
            show_helpMsg()
        else:
            color_out("red", "ERROR: 沒有相對應的指令", True)
    return

if __name__=='__main__':
    main()