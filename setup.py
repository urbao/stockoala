# This python script will help user run through all setup process

# define several useful info variables
from output import color_output
LANG="EN"
SYS="Linux"
USERNAME="koala"
DIRPATH="$HOME_DIR"

# determine what os platform it is
def iden_platform():
    import platform
    if platform.system()!="Windows" and platform.system()!="Linux":
        color_output("red", "I'm sorry your os platform is not supported(很遺憾地stockoala不支援你的作業系統)", True)
        color_output("yellow", "The program will close after 3s(三秒後setup將自動結束)", True)
        import time,sys
        time.sleep(3)
        sys.exit() 
    else:
        global SYS
        SYS=platform.system()
        color_output("white", "Platform check", False)
        color_output("green", "Pass", True)
        return

# let user choose the language
def pick_lang():
    color_output("white", "1. English", True)
    color_output("white", "2. 繁體中文\n", True)
    global LANG
    while True:
        color_output("white", "(1 or 2 ??) -> ", False)
        ans=input()
        if ans=="1":
            LANG="EN"
            color_output("white", "Update language to", False)
            color_output("green", LANG, True)
            break
        elif ans=="2":
            LANG="TW"
            color_output("white", "Update language to", False)
            color_output("green", LANG, True)
            break
        else:
            color_output("red", "[Error] Retry again(請重試一次)\n", True)

# Foreword
def foreword():
    if LANG=="EN":
        color_output("white", "Hi, Welcome to use stockoala", True)
    else:
        color_output("white", "嗨，歡迎使用stockoala", True)
    return 

# let user set their user name
def set_usrname():
    if LANG=="EN":
        color_output("white", "Enter your username: ", False)
    else:
        color_output("white", "輸入你的使用者名稱: ", False)
    global USERNAME
    USERNAME=input()
    return

# change directory based on the SYS variable
def chg_DIRPATH():
    import os
    global DIRPATH
    DIRPATH=os.path.expanduser("~")
    if SYS=="Linux":
        DIRPATH+="/Desktop/stockoala/"
    else:
        DIRPATH+="\\Desktop\\stockoala\\"
    return

# record the user data into a hidden file called ".config"
def updt_config():
    file_path=DIRPATH+".config"
    with open(file_path, 'w') as file:
        file.write("LANG:"+LANG+"\n")
        file.write("USERNAME:"+USERNAME+"\n")
        file.write("DIRPATH:"+DIRPATH+"\n")
        return

# afterword
def afterword():
    if LANG=="EN":
        color_output("yellow", "Hello, nice to meet you ["+USERNAME+"]", True)
        color_output("green", "[Successful] setup the stockoala\n", True)
        color_output("white", "The program will close after 3s", True)
    else:
        color_output("yellow", "哈囉，很高興認識你 ["+USERNAME+"]", True)
        color_output("green", "[成功] 完成設定stockoala\n", True)
        color_output("white", "三秒後setup將自動結束", True)
    import time,sys
    time.sleep(3)
    sys.exit() 

#### Combine all side-program into one singel setup python script ####
def main():
    pick_lang()
    iden_platform()
    foreword()
    set_usrname()
    chg_DIRPATH()
    updt_config()
    afterword()

if __name__=="__main__":
    main()
