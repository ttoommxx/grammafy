#!/bin/sh

echo "Select the tex file"
read
./modules/fff-2.2_read/fff

text=$(python3 grammafy.py)
echo "$text" # print everything but the last line
echo "Press to open the output"
xdg-open "$(cat opened_file_grammafied)"

rm opened_file
rm opened_file_grammafied