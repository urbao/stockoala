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

# print out whole text file
def color_file(filename, line_count):
    data=open(filename+".txt",'r').readlines()
    color_output("yellow","   ID  HIGH     LOW", True)
    for idx in range(line_count):
        if(idx==0): print(" ", end="") # for the first line offset
        data[idx]=data[idx].strip("\n").split("/")
        color_output("cyan", data[idx][0]+":", False)
        color_output("green", data[idx][1], False)
        if (len(data[idx][1])==6): print("  ", end="")
        elif (len(data[idx][1])==5): print("   ", end="")
        elif (len(data[idx][1])==4): print("    ", end="")
        elif (len(data[idx][1])==3): print("     ", end="")
        elif (len(data[idx][1])==2): print("      ", end="")
        elif (len(data[idx][1])==1): print("       ", end="")
        color_output("purple", data[idx][2]+"\n", False)
    return

# function that push the file to GitHub
def git_push():
    import os
    try:
        color_output("cyan", "----git add----", True)
        os.system("git add .")
        color_output("cyan", "----git commit----", True)
        os.system("git commit -m \"Update data\"")
        color_output("cyan", "----git push----", True)
        os.system("git push")
        color_output("cyan", "----result----", True)
        color_output("white", "Git Push:", False)
        color_output("green", "[DONE]\n", True)
    except:
        color_output("white", "Git Push:", False)
        color_output("red", "[FAIL]\n", True)
    return
