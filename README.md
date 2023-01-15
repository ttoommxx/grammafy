# grammafy

Version 0.2

This script serves the purpose of cleaning up tex files to a txt file that can be put into online writing checking software

## pre-requisites

Any python version should work, tested on Linux and Windows using Python 3.10 and 3.11.
If it doesn't do anything, install tkinter via
```
pip install tk
```

## how to use

### aggressive mode

On Windows, double click on WindowsRun.bat.
On Linux, run LinuxRun.sh.
Using the graphical selector, pick the main .tex file you want to clean.

### debugging mode (recommended)

The physolophy of the code is that once things are checked out from the old text, they are always removed. Essentially the code is made so that it's eating portion of the raw .tex file and command by command converting it into readable txt file.

Every command should end with one of the following symbols: ' ', '}', '{', '.', ',', ':', ';', '\n'. Ending with asterisk is reserved as a special behaviour for built-in functions, and as such custom command should not end with an asterisk.
end_command.txt can be modified to handle different endings.


WRITE ON HOW TO USE THE DEBUGGING TO MAKE IT WORK PERFECTLY




To do:
- finish cleaning up
- aggressive mode, removes all unknown commands
- include license
- include grammarly API directly
