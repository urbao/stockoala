#!/bin/bash

# this shell script will be the main part of 'stockoala'
# It controls all user behavior, and decide to run which python script 
# created by https://github.com/urbao for project 'stockoala'
# further info: https://github.com/urbao/stockoala
# feature: command line interface

#--------#--Basic Definition------------#


#---------------------------------------#


#------------Side Functions-------------#
# help function is show all valid commands when user typing help
function help()
{	
	# keep appending while the function increased
	echo "help		-- show all available commands"
	echo "col 	 	-- collect stock data"
	echo "ls 		-- show all data files with number"
	echo "show 		-- choose file and show with user-defined column size"
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
	return 0
}

#---------------------------------------#

#-----------Viewer Function-------------#
# list_files let user know which file one they want to view
function list_files()
{	
	print "cyan" "-------------- File List ---------------" "nl"
	idx=1
	filename_list=$(ls *.txt)
	for filename in $filename_list
	do
		space=$(printf '%*s' $((3-"${#idx}")) ' ')
		print "yellow" "$idx.$space" "nnl"
		print "white" "$filename" "nl"
		idx=$((idx+1))
	done
	print "cyan" "----------------------------------------" "nl"
	return 0
}

# choose_number is used by choose_file and file_viewer function (for file index and column limit)
# $1: input reminder
# $2: True/False; used to check if valid index check is needed or not
function choose_number()
{
	while(true)
	do
		print "purple" "$1" "nnl"
		read -r ans
		# use equal-tlide to comfirm digit or not
		if ! [[ $ans =~ ^[0-9]+$ ]];then print "red" "[ERROR] contains non-digit symbol" "nl"
		elif [ "$2" == False ];
		then 
			columns_limit_size="$ans"
			return 0
		elif [[ $ans -ge $idx || $ans == 0 ]];then print "red" "[ERROR] invalid file number" "nl"
		else
			# get filename based on idx, and return it
			idx=1
			for filename in $filename_list
			do
				# match file number
				if [ "$idx" == "$ans" ]
				then
				# store filename in GLOBAL VARIABLE wannaopen_filename, and leave
					wannaopen_filename="$filename"
					return 0
				# keep counting until file number matches
				else
					idx=$((idx+1))
				fi
			done
		fi
	done
}

# file_viewer open file and print contents out formattly
function file_viewer()
{
	list_files
	choose_number "Choose file number:" True
	choose_number "Choose column size:" False
	# get chose filename(using echo to receive result, not return(only accept exit code))
	# start readline and print out, counter used to count how many columns printed(5 columns limit)
	# msb is Most Siginificant Bit: identify stock id thousands digit, break stock into different part
	IFS='/' counter=0 msb=0
	while read -r -a line
	do
		# space 1,2 are used to perform data uniformly based on strinf length
		space1=$(printf '%*s' $((8-"${#line[1]}")) ' ')
		space2=$(printf '%*s' $((7-"${#line[2]}")) ' ')
		space3=$(printf '%*s' $((4)) ' ')
		# into another part of stock(based on the msb of stock id), create new segment
		if [[ $(("${line[0]}"/1000)) -gt "$msb" ]]
		then
			echo ""
			msb=$(("msb"+1))
			print "red" "\n>> [${msb}000 to ${msb}999]" "nl"
			# running the for-loop, print out corrseponding header
			for ((i=1; i<="$columns_limit_size"; i++))
			do
				if [ "$i" != 1 ] && [ "$i" != "$columns_limit_size" ]
				then
					print "white" "$space3" "nnl"
				fi
				print "cyan" "Stock ID     High     Low" "nnl"
			done
			echo ""
			counter=0
		fi
		# print out file content
		# line[0]: stock id
		# line[1]: high
		# line[2]: low
		print "yellow" "    ${line[0]}" "nnl"
		print "green" "$space1${line[1]}" "nnl"
		print "purple" "$space2${line[2]}" "nnl"
		# hit one line printout column limit
		if [[ "$counter" -ge $(("$columns_limit_size"-1)) ]]
		then
			print "nothing" "" "nl"
			counter=0 # reset counter for new row
		else
			print "spaceonly" "$space3" "nnl"	
			counter=$(("$counter"+1))
		fi
	done < "$wannaopen_filename"
	return 0
}
#---------------------------------------#


#------------Main Functions-------------#
# GLOBAL VARIABLE
wannaopen_filename=""
columns_limit_size=0
# Used CLI as mainline(like money tracker)
# since run.sh will already in dir
help
cd data/ || return
file_viewer
#---------------------------------------#
