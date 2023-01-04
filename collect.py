import date_time
import requests
import output
import prune
import combine

# get the start Monday date(DONT modify start_date)
start_date=str(date_time.get_date())

# use iterations to collect data from Mon. to Fri.
date=start_date
output.color_output("cyan", "\n==============$$$$===============", True)
for i in range(5): # THE 5 CAN CHANGED TO ANY LENGTH OF DAYS AS WE WANT
    requests.twse(date)
    prune.twse_rm_extras(date)
    requests.tpex(date)
    prune.tpex_rm_extras(date)
    date=str(date_time.add_1day(date))

# find weekly data of TWSE and TPEX
print("\n")
combine.weekly_data(start_date, "twse")
combine.weekly_data(start_date, "tpex")
print("\n")

# final combination of TWSE and TPEx file, and show some info
count=combine.final_combine(start_date)
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
output.color_output("white", "For more data details, use viewer to check the data files\n", True)
input("Press any key to exit...")
os.system('clear')
os.chmod(start_date+".txt", 0o444)
