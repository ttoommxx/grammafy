# grammafy

Version 1.0

FROM HERE - REMEMBER TO WRITE THAT NONE OF THE SYMBOLS (" ","{","}",".",",",":",";","[","]","(",")","$","\\","\n","\"","'","~","%") CAN BE INCLUDED IN THE PROGRAM NAME

This script serves the purpose of cleaning up tex files by creating a txt file, stripped of all commands, that can be fed to writing software. Formulas are substituted with the symbol `[_]`, and the other changes should be comprehensible.

I don't ask for money, please give a star if you have used my program :)

## installation and use

Needs Python >= 3.10. Download the last release and run grammafy.py from terminal
```
python3 grammafy.py
```
Select the main tex file by navigating with the arrows and pressing enter on it. The [terminal file manager](https://github.com/ttoommxx/pylePicker) was written with the help of AI (ChatGPT).

If you want the latest hotfixes, clone the main branch of this GitHub page.

## debugging mode

This script follows a strict philosophy: every command knows exactly what is doing and can only see the source tex file from where the command starts.

The script computes the following instructions:
1) Everything written before `\begin{document}` is immediately removed.
2) After such a command, the script unpacks all the included tex files and turns the tex file into a big string (source).
3) It starts scanning for certain symbols, which I call interactives:
```
("\\","{","}","$","%","~")
```
4) If it finds any of the above, it everything to the output file (clean), and executes an action depending on the symbol.
5) If the special character ``\\`` is selected, the script, after looking for some simple interactives, checks if the command following ``\\`` is present in the folder "./exceptions/routines_custom" first, then "./exceptions/routines" and if in neither, it skips the command with its arguments.
6) Every time a routine is found and loaded, the source file is updated by removing everything before ``\\`` and the routine is executed as text within the script. In particular, every routine can see the source file (but it's updated, so can't see anything before the command) and can see the clean string too.
6.1) Two special routines "begin" and "end" look for subroutines within the folders "./exceptions/subroutines/".
7) At the end of execution, the script has produced a _grammafied.txt file, which the clean output, a _list_unknowns.txt, with unknown commands, and a _list_log_command.txt, with unknown "begin"-commands.

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

## disclaimers

This project is not intended to be a fully working application, at least at the moment. It was developed to facilitate correcting typos in my dissertation thesis, and because it works well enough I thought sharing it with everyone would be a good idea. If you want to help me with this project or have any suggestions, do not hesitate to reach out to me by email!
