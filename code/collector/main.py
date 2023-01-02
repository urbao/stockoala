import requests
import output
import parse

# get the start Monday date(DONT modify start_date)
start_date=str(requests.get_date())

# make directory to store data file
import os
os.chdir(str("/home/eason/Desktop/stock/data"))

# use iterations to collect data from Mon. to Fri.
date=start_date
output.color_output("cyan", "\n==============$$$$===============", True)
for i in range(5): # THE 5 CAN CHANGED TO ANY LENGTH OF DAYS AS WE WANT
    requests.twse(date)
    parse.twse_rm_extras(date)
    requests.tpex(date)
    parse.tpex_rm_extras(date)
    date=str(requests.add_1day(date))

# find weekly data of TWSE and TPEX
print("\n")
parse.weekly_data(start_date, "twse")
parse.weekly_data(start_date, "tpex")
print("\n")

# final combination of TWSE and TPEx file, and show some info
count=parse.final_combine(start_date)
output.color_output("yellow", "\nTWSE:", False)
output.color_output("green", str(count[0]), True)
output.color_output("cyan", "TPEX:", False)
output.color_output("green", str(count[1]), True)
output.color_output("purple", "Total:", False)
output.color_output("green", str(count[2]), True)
output.color_output("cyan", "==============$$$$===============", True)

# show data details, and finally lock the file
import os
os.rename(start_date+"[total].txt", start_date+".txt") # rename for simplicity
output.git_push()
os.system('notify-send -u critical -i /home/eason/Desktop/stock/collector/collector.png "Stock Collect [Done]"')
input("Press any key to continue...")
os.system('clear')
output.color_file(start_date, count[2])
os.chmod(start_date+".txt", 0o444)
