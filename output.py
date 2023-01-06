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

# print_col_name will print Stock id/high/low name
def print_col_name(column_size):
     # start printing title
    space=' '
    for i in range(int(column_size)):
        # between column, insert space for better lookng
        if(i!=0 and i!=int(column_size)):
            print(4*space, end='')
        color_output("cyan", "Stock ID     High     Low", False)
    print("") # newline
    return

# print_title function is used when new section is genrated
def print_title(header):
    # dynamically print out dash-line, based on the terminal width
    import os
    # return type: list; 1st item is height; 2nd item is width
    height_width=os.popen('stty size', 'r').read().split()
    for i in range(int(height_width[1])):
        if i==int((int(height_width[1])/2)-len(str(header))+1):
            color_output("red", str(header), False)
            i+=len(str(header)) # since the header is 14 words long
        else:
            color_output("red", "\b-", False)
    print("")
    return

# print datafiles beautifully
def file_content(filename, column_size):
    print_title(filename) # print out filename for much more readibility
    import get
    filedata=get.file_data(filename)
    MSB=0 # for checking section based on thousands number
    col_count=0  # for checking current printed columns
    space=' ' # for print out adequate space
    # run through all lines, and break it into different stock id
    for line in filedata:
        # check if going to new section
        if(int(int(line[0])/1000)>MSB):
            color_output("newline", "", True)
            MSB+=1
            header="["+str(MSB)+"000~"+str(MSB)+"999] "
            print_title(header)
            print_col_name(column_size)
            col_count=0 # reset to zero, since newline
        # start printing out data content
        print(4*space, end='')
        color_output("yellow", line[0], False)
        print((8-len(line[1]))*space, end='')
        color_output("green", line[1], False)
        print((7-len(line[2]))*space, end='')
        color_output("purple", line[2], False)
        # check if column exceed, if does, have a newline
        if(col_count>=int(column_size)-1):
            print("") # newline
            col_count=0
        else:
            print(4*space, end='')
            col_count+=1    
    print("")
    return

