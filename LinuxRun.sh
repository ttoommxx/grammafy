#!/bin/sh

text=$(python grammafy.py)
echo "$text" | sed '$d' # print everything but the last line
echo "Press enter to open the output"
read -n1 KEY
if [[ "$KEY" == "" ]]
then
  xdg-open "${text##*$'\n'}" # only takes the last variable
fi
