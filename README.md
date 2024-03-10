# grammafy 1.4.2

This script serves the purpose of cleaning up tex files by creating a txt file, stripped of all the commands, that can be fed to typying software such as Grammarly. Formulas are substituted with the symbol `[_]`, and the other changes should be comprehensible.

I don't ask for money, but please give a star to the repository if you have found my program useful :)

## installation and use

Needs Python >= 3.10. Download the latest release and run grammafy.py from terminal
```
python3 grammafy.py
```
Select the main tex file by navigating with the arrows and pressing enter on it (see [terminal file manager](https://github.com/ttoommxx/pylePicker) )

If you want the latest hotfixes, clone the main branch of this GitHub page.

## debugging mode

This script follows a strict philosophy: every command knows exactly what is doing and nothing else, and can only see the tex file as a string (`source`), the cleaned-up file (`clean`) and the file path.

The script computes the following instructions:
1) Everything written before `\begin{document}` is immediately removed and the rest of the tex file is saved into a big string called `source.text`.
2) The program scans `source.text` looking for the following symbols:
```
\ , { , } , $ , % , ~
```
3) If it finds any of the above, it prints everything to `clean.text` up until such symbol, by calling `clean.add(text)`, and executes an action depending on the symbol.
4) If the special character ``\`` is found, the script interprets the command as everything in between `\` and
```
{ , } , . , , , : , ; , [ , ] , ( , ) , $ , \ , \n , " , ' , ~
```
At this point, I wrote most of the built in commands. If you want to add your own, please add to any of the custom py modules following the provided templates. Also the void files constitute a list of void commands.
5) If the command if found, the index of `source` is moved right at the end of it and the command is run.
6) I included two special routines, `begin` and `end` that have their own folder modules.
7) At the end of execution, the script writes `clean.text` in a file ending with `_grammafied.txt`, and saves the unknown commands in a file ending with `_unknowns.txt`.

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

This project is not intended to be a fully working application, at least at the moment. It was developed to facilitate correcting typos in my dissertation thesis, and because it works well enough I thought that sharing it with everyone would be a good idea. If you want to help me with this project or have any suggestions, do not hesitate to reach out to me by email.

# to do

- I am thiking of adding pre and post operations.