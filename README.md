# grammafy

Version 0.4

This script serves the purpose of cleaning up tex files by creating to a txt file, stripped of all commands, that can be fed to writing softwares. Formulas are substituted with the symbol [1], and the other changes should be comprehensible.

## installation and use

Any python version should work, tested on Linux and Windows using Python 3.10 and 3.11. Download the repo with
```
git clone https://github.com/ttoommxx/grammafy
```
and install tkinter. On Arch by typing
```
sudo pacman -S tk
```
and on Ubuntu via
```
sudo apt install python3-tk
```
(check for your OS). Once everything is set up, simply run
```
./LinuxRun.sh
```
and using the graphical selector, pick the main .tex of your project.

## debugging mode

WRITE HOW TO USE THE DEBUGGING TO UNDERSTAND HOW TO IMPLEMENT YOUR MODULES

This script follows a strict phylosophy: every command knows exactly what is doing and can only see the source tex file from where the command starts. After executing 

The physolophy of the code is that once things are checked out from the old text, they are always removed. Essentially the code is made so that it's eating portion of the raw .tex file and command by command converting it into readable txt file.

Every command should end with one of the following symbols:
```
' ', '}', '{', '.', ',', ':', ';', '\n'
```
Ending with asterisk is reserved as a special behaviour for built-in functions, and as such custom command should not end with an asterisk.
end_command.txt can be modified to handle different endings.


WRITE ON HOW TO USE THE DEBUGGING TO MAKE IT WORK PERFECTLY




To do:
- write good doc
- include license
- include grammarly API directly
