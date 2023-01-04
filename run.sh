#!/bin/bash

# this shell script will be the main part of 'stockoala'
# It controls all user behavior, and decide to run which python script 
# created by https://github.com/urbao for project 'stockoala'
# further info: https://github.com/urbao/stockoala

#--------#--Basic Definition------------#


#---------------------------------------#


#------------Side Functions-------------#
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
	return
}

# git_ps used to push data to GitHub after collecting
function git_ps()
{
	return
}

# choose_file let user pickup which file one they want to view
# return type: $ans is the filenumber
function choose_file()
{	
	print "cyan" "-- Choose file number you want to check" "nl"
	idx=1
	filename_list=$(ls *.txt)
	for filename in $filename_list
	do
		space=$(printf '%*s' $((3-"${#idx}")) ' ')
		print "yellow" "$idx.$space" "nnl"
		print "white" "$filename" "nl"
		idx=$((idx+1))
	done
	while(true)
	do
		print "purple" "\nChoose file number:" "nnl"
		read -r ans
		# use equal-tlide to comfirm digit or not
		if ! [[ $ans =~ ^[0-9]+$ ]]
		then
			print "red" "[ERROR] contains non-digit symbol" "nl"
		elif [[ $ans -ge $idx || $ans == 0 ]]
		then
			print "red" "[ERROR] invalid file number" "nl"
		else
			return "$ans"
		fi
	done
}

# file_viewer open file and print contents out formattly
# $1: file number
function file_viewer()
{
	idx=1
	filename_list=$(ls *.txt)
	for filename in $filename_list
	do
		# match file number
		if [ "$idx" == "$1" ]
		then
			openfile="$filename"
			break
		# keep counting until file number matches
		else
			idx=$((idx+1))
		fi
	done
	while read -r line
	do 
		# print out file content	 
	done < "$openfile"
	
	return
}

#---------------------------------------#


#------------Main Functions-------------#
# since run.sh will already in dir
cd data/ || return
# choose file and assign filenumber to num variable
choose_file
num=$?
file_viewer "$num"
#---------------------------------------#
