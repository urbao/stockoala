#!/bin/bash

# install.sh support much friendly install method
# which will install stockoala only needed one simple command
# including setup for git init, and bla bla bla

#----------Default Value-----------#
# Some root path might need access, so print out advanced statment
folder="stockoala"
dirpath="$HOME/Desktop/"
dsktpath="$HOME/.local/share/applications/"
iconpath="/usr/share/icons/hicolor/512x512/"
#----------------------------------#

#---------------------Functions-----------------------#
# print fnction with color and newline/sameline options
# nl: NewLine/ nnl: No NewLine
function print(){
	local c_code=0
	# color c_code chck
	if [ "$1" == "yellow" ]; then c_code="33m" 
	elif [ "$1" == "green" ]; then c_code="32m" 
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

# git_init function make sure git is inited in ~/.../stockoala directory
function git_init(){
	
	return
}

# update stock_data to GitHub using 'git add ./', and asking users' repo link
function updt_data(){

	return
}

# dsktp function will create a desktop file based on the config
function new_dsktp(){

	return
}

#-----------------------------------------------------#


#------------------Main Function----------------------#
print "white" "----- This is installation of stockoala -----" "nl"
print "yellow" "> Some process might need pwd for sudo\n" "nl"

#-----------------------------------------------------#


