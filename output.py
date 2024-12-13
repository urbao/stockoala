# add package tht can run ASCII code in Windows OS
import colorama 
colorama.init()

# print line with color
def color_out(color="white", line="NoContent", newline=True):
    if color=="red":
            code="31m"
    elif color=="yellow":
        code="33m"
    elif color=="green":
        code="32m"
    elif color=="cyan":
        code="36m"
    elif color=="purple":
        code="35m"
    else:
        code="37m" # white
    if newline:
        print("\033[1;"+code+line+"\033[0m")
    else:
        print("\033[1;"+code+line+"\033[0m", end=" ")
    return

colorama.deinit()