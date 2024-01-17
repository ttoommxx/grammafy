#----------------------------------------
# BUILT-IN FUNCTIONS
#----------------------------------------

import os

def _reprint(source, clean, command, folder_path):
    """ add the command to clean the command """
    clean.add(command)

def _curly(source, clean, command, folder_path):
    """ move to the end of curly brackets """
    source.move_index("}")

def _curly_curly(source, clean, command, folder_path):
    """ move to the end for 2 consecutive curly brackets """
    source.move_index("}")
    source.move_index("}")

def _color(source, clean, command, folder_path):
    """ add color to source and move to the end of curly brackets """
    clean.add("Color:")
    i = source.text.find( "}" )
    clean.add(source.text[ 1:i ].upper())
    source.index += i+1

def _footnote(source, clean, command, folder_path):
    """ add footnote to source and move to the end of nested curly brackets """
    i = 1
    j = i # index for open brackets
    while i >= j and j > 0 :
        i = source.text.find( "}",i ) +1
        j = source.text.find( "{",j ) +1

    # add the text in the footnote to the queue in parenthesis
    source.add("(FOOTNOTE: " + source.text[ 1:i-1 ] + ")")
    source.root.index += i

def _include(source, clean, command, folder_path):
    """ responds to \include command and adds the new source to the head of source. The included files need to be in the same folder """
    i = source.text.find("}")
    include_path = source.text[ 1:i ]
    if not include_path.endswith(".tex"): # if the extension is not present
        include_path += ".tex"
    with open(f"{folder_path}{include_path}", encoding="utf-8") as include_tex:
        source.add( include_tex.read() )
    source.root.index += i+1

def _print_curly(source, clean, command, folder_path):
    """ [_] to clean when meeting curly brackets and move to the end of curly brackets """
    clean.add("[_]")
    source.move_index("}")

def _print_square_curly(source, clean, command, folder_path):
    """ add [_] for clean and move to the end of square if present, and then curly brackets """
    clean.add("[_]")
    if source.text[0] == "[":
        source.move_index("]")
    source.move_index("}")

from exceptions import sub_begin

def _begin(source, clean, command, folder_path):
    """ responds to the command being and move to the function begin and its subroutines """
    i = source.text.find("}") # right next after the brackets
    command = source.text[ 1:i ] # remove asterisk if any
    source.move_index("}")
    sub_begin.interpret(source, clean, command, folder_path)
        
from exceptions import sub_end
        
def _end(source, clean, command, folder_path):
    """ responds to the command end and move to the function end and its subroutines """
    i = source.text.find("}")
    command = source.text[ 1:i ]
    source.move_index("}")
    sub_end.interpret(source, clean, command, folder_path)

# special commands (not include command to avoid string problems)

def _new_line(source, clean, folder_path):
    """ add a new line to clean """
    clean.add("\n")
    source.index += 1

def _square_equation(source, clean, folder_path):
    """ add [_] when meeting an equation called via \[ and move index to the end if it """
    i = source.text.find( "\\]" )
    clean.add("[_]")
    if source.text[:i].rstrip()[-1] in [",", ";", "."]: # add punctuation to non-inline equations
        clean.add(source.text[:i].rstrip()[-1])
    source.move_index( "\\]" )

def _round_equation(source, clean, folder_path):
    """ add [_] when meeting an equation called via \( and move index to the end if it """
    i = source.text.find( "\\)" )
    clean.add("[_]")
    if source.text[:i].rstrip()[-1] in [",", ";", "."]: # add punctuation to non-inline equations
        clean.add(source.text[:i].rstrip()[-1])
    source.move_index( "\\)" )

def _apostrofe(source, clean, folder_path):
    """ skip letter when meeting an apostrofe """
    if source.text[1] in ("a","e","i","o","u"):
        source.index += 1

def _tilde(source, clean, folder_path):
    """ add tilde to clean """
    clean.add("~")
    source.index += 1

def _null_function(source, clean, folder_path):
    """ null function, does nothing """


#----------------------------------------
# VARIABLES
#----------------------------------------

from exceptions.routines_custom import void_c

void = (
    "centering",
    "small",
    "large",
    "Large",
    "newpage",
    "textbf",
    "textit",
    "emph",
    "maketitle",
    "tableofcontents",
    "footnotesize",
    "selectfont",
    "author",
    "title",
    "date",
    "Huge",
    "huge",
    "underline",
    "chapter",
    "section",
    "subsection",
    "subsubsection",
    "section*",
    "subsection*",
    "subsubsection*",
    "text",
    "bbox",
    "clearpage",
    "appendix",
    "p",
    "S",
    "compat",
    "bf",
    "em",
    "printbibliography",
    "bigskip",
    "mbox",
    "preprint",
    "affiliation",
    "noindent",
    "texorpdfstring",
    "it",
    "address",
    "thanks",
    "textsc",
    "texttt"
)

from exceptions.routines_custom import dic_commands_c

dic_commands = {
    "addchap":_curly,
    "addsec":_curly,
    "begin":_begin,
    "bibliography":_curly,
    "bibliographystyle":_curly,
    "chaptermark":_curly,
    "cite":_print_square_curly,
    "color":_color,
    "cref":_print_curly,
    "Cref":_print_curly,
    "email":_curly,
    "end":_end,
    "eqref":_print_curly,
    "fontfamily":_curly,
    "footnote":_footnote,
    "hspace":_curly,
    "include":_include,
    "includegraphics":_curly,
    "input":_include,
    "label":_curly,
    "pagenumbering":_curly,
    "pagestyle":_curly,
    "ref":_print_curly,
    "renewcommand":_curly_curly,
    "setlength":_curly_curly,
    "thispagestyle":_curly,
    "vspace":_curly,
    "&":_reprint,
    "%":_reprint,
    "#":_reprint
}

special_commands = {
    "[":_square_equation,
    "(":_round_equation,
    "\"":_apostrofe,
    "'":_apostrofe,
    "\\":_new_line,
    "\n":_new_line,
    "~":_tilde,
}

#----------------------------------------
# INTERPRETER
#----------------------------------------

def interpret(source, clean, command, folder_path):
    """ this is the custom interpreter that recalls first custom subroutines, then built-in subroutines and then skip the command if not recognised """
    if command:
        if command in void or command in void_c:
            pass
        elif command in dic_commands_c:
            dic_commands_c[command](source, clean, command, folder_path)
        elif command in dic_commands:
            dic_commands[command](source, clean, command, folder_path)
        else:
            while source.text[0] in ["{","["]: # check if opening and closing brackets
                if source.text[0] == "{":
                    i = source.text.find("{",1)
                    j = source.text.find("}",1)
                    while 0 < i < j:
                        i = source.text.find("{",i+1)
                        j = source.text.find("}",j+1)
                    source.index += j+1
                else:
                    i = source.text.find("[",1)
                    j = source.text.find("]",1)
                    while 0 < i < j:
                        i = source.text.find("[",i+1)
                        j = source.text.find("]",j+1)
                    source.index += j+1
            clean.aggro.add(command)
    else: # empty string
        command = source.text[0]
        if command in special_commands:
            special_commands[command](source, clean, folder_path)
        else:
            clean.add(" ")
            source.index += 1


#----------------------------------------
