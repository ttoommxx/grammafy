# grammafy

Version 0.3

This script serves the purpose of cleaning up tex files by creating to a txt file, stripped of all commands, that can be put into an writing software. Formulas are substituted with the symbol [1], and the other changes should be comprehensible.

## installation

Any python version should work, tested on Linux and Windows using Python 3.10 and 3.11.
```
git clone https://github.com/ttoommxx/grammafy
```
install tkinter on your operating system. For example, on Arch
```
sudo pacman -S tk
```
or on Ubuntu
```
sudo apt install python3-tk
```

## how to use

On Windows, double click on WindowsRun.bat.
On Linux, run LinuxRun.sh.
Using the graphical selector, pick the main .tex file you want to clean.

### aggressive mode (not recommended)

Using aggressive mode, every time program encounters an unknown command, it would discard it along with all square [] and curly {} brackets that are consecutive to the program.

### debugging mode (recommended)

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
