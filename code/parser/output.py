# print line with color (green/red/yellow/cyan/purple/white)
def color_output(color, line, newline):
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

# print out reminder
def reminder():
    color_output("cyan","-- Use most recent date for analyzing", True)
    color_output("cyan","-- Default traceback for 12 weeks", True)
    color_output("red", "-- Make sure update to latest data\n", True)
    return
