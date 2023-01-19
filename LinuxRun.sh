#!/bin/sh

text=$(python grammafy.py)
echo "$text" | sed '$d' # print everything but the last line
echo "Do you want to open the output? Y/N"
read answer
if [ "${answer,}" = "y" ]; then 
	xdg-open ${text##*$'\n'} # only takes the last variable
fi
