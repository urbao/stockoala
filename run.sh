#!/bin/bash

# this shell script will be the main part of 'stockoala'
# It controls all user behavior, and decide to run which python script
# created by https://github.com/urbao for project 'stockoala'
# further info: https://github.com/urbao/stockoala
# feature: command line interface

#Basic Definition(Dont Change this part, installation will update this part)
#---------------------------------------#



#------------Side Functions-------------#
# help function is show all valid commands when user typing help
function help()
{
	# keep appending while the function increased
	echo "help		-- show all available commands"
	echo "pwd		-- print current directory"
	echo "collect 	-- collect stock data"
	echo "ls 		-- show all data files with number"
	echo "show 		-- choose file and show with user-defined column size"
	echo "parse		-- find all stock in reverse-point"
	echo "clear		-- clear the screen"
	echo "exit		-- exit the program"
	return 0
}

# print fnction with color and newline/sameline options
# nl: NewLine/ nnl: No NewLine
function print()
{
	local c_code=0
	# color c_code chck
	if [ "$1" == "yellow" ]; then c_code="33m" 
	elif [ "$1" == "green" ]; then c_code="32m" 
	elif [ "$1" == "red" ]; then c_code="31m" 
	elif [ "$1" == "cyan" ]; then c_code="36m" 
	elif [ "$1" == "purple" ]; then c_code="35m"
	#white output(Default)
	else c_code="37m" 
	fi
	# combine c_code with printed line(string combination)
	c_code+="$2"
	# new line or not
	# 'echo -e' enables color hex code identification
	if [ "$3" == "nl" ]
	then
		echo -e  "\e[1;${c_code}\e[0m"
	# '-n' parameter means no newline
	else
		echo -n -e "\e[1;${c_code} \e[0m"
	fi
	return 0
}

# git_ps used to push data to GitHub after collecting(alreadt init at installing)
function git_ps()
{	
	cd "${dirpath}data/" || return
	print "cyan" "------------Git Add--------------" "nl"
	git add .
	print "cyan" "-----------Git Commit------------" "nl"
	datetime=$(date '+%Y/%m/%d')
	git commit -m "Update data at $datetime"
	print "cyan" "------------Git Push-------------" "nl"
	git push -u origin master
	print "cyan" "------------Complete-------------" "nl"
	return 0
}

#---------------------------------------#

#-----------Viewer Function-------------#
# list_files let user know which file one they want to view
function list_files()
{	
	cd "${dirpath}data/" || return
	print "cyan" "-------------- File List ---------------" "nl"
	idx=1
	filename_list=$(ls -- *.txt)
	for filename in $filename_list
	do
		# space for filenumber
		space=$(printf '%*s' $((3-"${#idx}")) ' ')
		print "yellow" "$idx.$space" "nnl"
		if [ $(("$idx"%2)) == 1 ]
		then
			print "white" "$filename     " "nnl"
		else
			print "white" "$filename" "nl"
		fi
		idx=$((idx+1))
	done
	print "cyan" "----------------------------------------" "nl"
	return 0
}

#---------------------------------------#


#------------Main Functions-------------#
# Used CLI as mainline(like money tracker)
# since run.sh will already in dir
while true
do
	print "purple" "\n${usrname}:" "nnl"
	IFS=" " read -r input
	if [ "$input" == "" ];then continue
	elif [ "$input" == "pwd" ]; then pwd
	elif [ "$input" == "exit" ]; then exit
	elif [ "$input" == "clear" ]; then clear
	elif [ "$input" == "help" ]; then help
	elif [ "$input" == "ls" ];
	then
		list_files
	elif [ "$input" == "show" ];
	then
		# list out all avalable options
		list_files
		# back to last dir, execute python show.py
		cd "$dirpath" || return
		python3 show.py		
	elif [ "$input" == "collect" ];
	then
		cd "$dirpath" || return
		python3 collect.py
		mv -- *.txt data/ # move the data file into data dir
		git_ps # push to GitHub for backup
		cd "$dirpath/data/" ||return
		chmod 444 -- *.txt
	else print "red" "Error: Invalid command\n" "nl"
	fi
done
#---------------------------------------#
