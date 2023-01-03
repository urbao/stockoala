from output import color_output

def yes_no(date):
    while(True):
        color_output("cyan", "Do you want to analyze", False)
        color_output("yellow", str(date), False)
        color_output("cyan", "data?", False)
        color_output("purple", "[Y/n]", False)
        ans=input("")
        if(ans=="Y" or ans=="y"): return "Yes"
        elif(ans=="N" or ans=="n"): return "No"
        else: color_output("red", "[ERROR] Invalid Response\n", True)

# get file list in dir with sorting descending way
def file_list(path):
    import os
    file_list=os.listdir(path)
    file_list.sort(reverse=True)
    return file_list

def file_line_count(file1):
    count=0
    for row in open(file1): 
        count += 1
    return count

# get file data with tuple in list in a single file
def file_data(file1):
    with open(file1, 'r') as f:
        file_data=f.readlines()
        for idx in range(file_line_count(file1)):
            file_data[idx]=file_data[idx].strip("\n").split("/")
        f.close()
    return file_data

# get all data files to read-only mode
def read_only(file_path):
    import os
    files=file_list(file_path)
    os.chdir(file_path)
    for file1 in files:
        if(file1!=".git" and file1!="README.md"):
            os.chmod(file1, 0o444) # 0o means octal representation
    return

# get all data files to read-write mode
def read_n_write(file_path):
    import os
    files=file_list(file_path)
    os.chdir(file_path)
    for file1 in files:
        if(file1!=".git" and file1!="README.md"):
            os.chmod(file1, 0o664) # 0o means octal representation
    return
