# grammafy

Version 0.7

This script serves the purpose of cleaning up tex files by creating a txt file, stripped of all commands, that can be fed to writing software. Formulas are substituted with the symbol `[_]`, and the other changes should be comprehensible.

## installation and use

Any new python version should work, tested on Arch Linux using Python 3.10 and 3.11. Install pynput via pip
```
pip install pynput
```
download the repo with
```
git clone https://github.com/ttoommxx/grammafy
```
and run grammafy.py from terminal (see WARNING)
```
python3 grammafy.py
```
To select the tex file use the arrows via the [terminal file manager](https://github.com/ttoommxx/pylePicker).

## debugging mode

This script follows a strict philosophy: every command knows exactly what is doing and can only see the source tex file from where the command starts.

The script computes the following instructions:
1) Everything written before `\begin{document}` is immediately removed.
2) After such a command, the script unpacks all the included tex files and turns the tex file into a big string (SOURCE).
3) It starts scanning for certain symbols, which I call interactives:
```
['\\','{','}','$','%','~']
```
4) If it finds any of the above, it everything to the output file (CLEAN), and executes an action depending on the symbol.
5) If the special character ``\\`` is selected, the script, after looking for some simple interactives, checks if the command following ``\\`` is present in the folder "./exceptions/routines_custom" first, then "./exceptions/routines" and if in neither, it skips the command with its arguments.
6) Every time a routine is found and loaded, the SOURCE file is updated by removing everything before ``\\`` and the routine is executed as text within the script. In particular, every routine can see the SOURCE file (but it's updated, so can't see anything before the command) and can see the CLEAN string too.
6.1) Two special routines "begin" and "end" look for subroutines within the folders "./exceptions/subroutines/".
7) At the end of execution, the script has produced a _grammafied.txt file, which the CLEAN output, a _list_unknowns.txt, with unknown commands, and a _list_log_command.txt, with unknown "begin"-commands.

If you want to customise the script, you can add a routine/subroutine into the _custom directories and can override default commands like that.
Commands that output nothing can be included in the void_custom.txt file, similarly for begin subroutines.

# WARNING

The script can handle pretty much everything and will always reach completion, under the assumption that the file compiles properly (though the script doesn't compile). There might be instances where it gives the wrong output. This is mostly when the tex file is poorly written. For example, when using nested equations like
```
$$ (e^x)^{-1} \text{ $$ = $$ } e^{-x} $$. 
```
The script does handle properly nested unknown commands such as
```
\begin{hello} This environemnt does nothing, \begin{hello} as you can see \end{hello} \end{hello}.
```
When writing a (custom) subroutine, it is not necessary to include the symbol *. The script is written so that such a symbol is simply ignored.

Because pynput hasn't been ported to Wayland yet, on Linux it is necessary to run terminal under Xwayland, for example use Xterm.

## to do

- include typing assistant cloud-based software APIs.

## disclaimers

This project is not intended to be a fully working application, at least at them moment. It was developed to facilitate correcting typos on my dissertation thesis, and because it works well enough I thought sharing it with everyone would be a good idea. If you want to help me with this project or have any suggestion, do not hesitate to reach out to me by email!
