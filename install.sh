#!/bin/bash

# install.sh support much friendly install method
# which will install stockoala only needed one simple command
# including setup for git init, and bla bla bla

#----------Default Value-----------#
# Some root path might need access, so print out advanced statment
# This three default value can be modified based on your preference
# HOWEVER, the path should be right, or error might occur
usrname="urbao"
dirpath="$HOME/Desktop/stockoala/"
dsktpath="$HOME/.local/share/applications/"
iconpath="/usr/share/icons/hicolor/512x512/"
#----------------------------------#

#---------------------Functions-----------------------#
# print fnction with color and newline/sameline options
# nl: NewLine/ nnl: No NewLine
function print()
{
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
	return 0
}

# confirm function make user have a 2nd chance regretting
function confirm()
{
	while(true)
	do
		print "purple" "Continue installation or Abort ??? [Y/n]" "nnl"
		read -r ans
		if [ "${ans,,}" == "y" ]
		then
			return 0
		elif [ "${ans,,}" == "n" ]
		then
			print "white" "Abort installation..." "nl"
			print "white" "----------------------------------\n" "nl"
			read -r -p "Press any key exit..."
			exit
		else
			print "yellow" "Error: invalid input\n" "nl"
			continue
		fi
	done
}

# dsktp function will create a desktop file based on the config
function new_dsktp()
{
	print "yellow" "new desktop file" "nl"
	cd "$dirpath" || return  
	mkdir data
	# group all dekstop file content and append to stockoala.desktop
	{
		echo [Desktop Entry]
		echo Name=stockoala
		echo Exec="${dirpath}run.sh"
		echo Icon="${iconpath}icon.png"
		echo Terminal=true
		echo Type=Application
	} >> stockoala.desktop
	return 0
}

# mv all needed files to its corresponding location
function chmod_+x_mv_files()
{
	# chmod to execution
	print "yellow" "chmod +x for files" "nl"
	chmod +x run.sh 
	chmod +x stockoala.desktop 
	# desktop file
	print "yellow" "moving .desktop file to $dsktpath" "nl"
	sudo mv stockoala.desktop "$dsktpath"
	update-desktop-database "$dsktpath"
	# icon.png
	print "yellow" "moving icon.png to $iconpath" "nl"
	sudo mv icon.png "$iconpath"	
	return 0
}

# save_addr function: save the address to run.sh for further usage
function save_addr()
{	
	# -i: permanently change file content
	# 10: append data after line 10
	print "yellow" "updating user info" "nl"
	sed -i "10 a usrname=\"$usrname\"\ndirpath=\"$dirpath\"\n" run.sh
	sed -i "10 a datapath=\"${dirpath}data/\"\n" parse.py
	return 0
}

#-----------------------------------------------------#


#------------------Main Function----------------------#
print "white" "----- stockoala installation -----" "nl"
print "yellow" "> Some process might need pwd for sudo" "nl"
print "yellow" "> Default value in install.sh can be changed" "nl"
print "yellow" "> Make sure read README before continue\n" "nl"
# check once before conitnue(leave or install)
confirm
print "white" "------------ install -------------" "nl"
new_dsktp
chmod_+x_mv_files
save_addr
print "purple" "Status:" "nnl"
print "green" "[Finished]" "nl"
print "white" "----------------------------------\n" "nl"
#-----------------------------------------------------#


