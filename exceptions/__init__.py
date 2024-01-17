#----------------------------------------
# BUILT-IN FUNCTIONS
#----------------------------------------

import os

def _reprint(SOURCE, CLEAN, command, folder_path):
    """ add the command to CLEAN the command """
    CLEAN.add(command)

def _curly(SOURCE, CLEAN, command, folder_path):
    """ move to the end of curly brackets """
    SOURCE.move_index("}")

def _curly_curly(SOURCE, CLEAN, command, folder_path):
    """ move to the end for 2 consecutive curly brackets """
    SOURCE.move_index("}")
    SOURCE.move_index("}")

def _color(SOURCE, CLEAN, command, folder_path):
    """ add color to SOURCE and move to the end of curly brackets """
    CLEAN.add("Color:")
    i = SOURCE.text.find( "}" )
    CLEAN.add(SOURCE.text[ 1:i ].upper())
    SOURCE.index += i+1

def _footnote(SOURCE, CLEAN, command, folder_path):
    """ add footnote to SOURCE and move to the end of nested curly brackets """
    i = 1
    j = i # index for open brackets
    while i >= j and j > 0 :
        i = SOURCE.text.find( "}",i ) +1
        j = SOURCE.text.find( "{",j ) +1

    # add the text in the footnote to the queue in parenthesis
    SOURCE.add("(FOOTNOTE: " + SOURCE.text[ 1:i-1 ] + ")")
    SOURCE.root.index += i

def _include(SOURCE, CLEAN, command, folder_path):
    """ responds to \include command and adds the new SOURCE to the head of SOURCE. The included files need to be in the same folder """
    i = SOURCE.text.find("}")
    include_path = SOURCE.text[ 1:i ]
    if not include_path.endswith(".tex"): # if the extension is not present
        include_path += ".tex"
    with open(f"{folder_path}{include_path}", encoding="utf-8") as include_tex:
        SOURCE.add( include_tex.read() )
    SOURCE.root.index += i+1

def _print_curly(SOURCE, CLEAN, command, folder_path):
    """ [_] to CLEAN when meeting curly brackets and move to the end of curly brackets """
    CLEAN.add("[_]")
    SOURCE.move_index("}")

def _print_square_curly(SOURCE, CLEAN, command, folder_path):
    """ add [_] for CLEAN and move to the end of square if present, and then curly brackets """
    CLEAN.add("[_]")
    if SOURCE.text[0] == "[":
        SOURCE.move_index("]")
    SOURCE.move_index("}")

from exceptions import sub_begin

def _begin(SOURCE, CLEAN, command, folder_path):
    """ responds to the command being and move to the function begin and its subroutines """
    i = SOURCE.text.find("}") # right next after the brackets
    command = SOURCE.text[ 1:i ] # remove asterisk if any
    SOURCE.move_index("}")
    sub_begin.interpret(SOURCE, CLEAN, command, folder_path)
        
from exceptions import sub_end
        
def _end(SOURCE, CLEAN, command, folder_path):
    """ responds to the command end and move to the function end and its subroutines """
    i = SOURCE.text.find("}")
    command = SOURCE.text[ 1:i ]
    SOURCE.move_index("}")
    sub_end.interpret(SOURCE, CLEAN, command, folder_path)

# special commands (not include command to avoid string problems)

def _new_line(SOURCE, CLEAN, folder_path):
    """ add a new line to CLEAN """
    CLEAN.add("\n")
    SOURCE.index += 1

def _square_equation(SOURCE, CLEAN, folder_path):
    """ add [_] when meeting an equation called via \[ and move index to the end if it """
    i = SOURCE.text.find( "\\]" )
    CLEAN.add("[_]")
    if SOURCE.text[:i].rstrip()[-1] in [",", ";", "."]: # add punctuation to non-inline equations
        CLEAN.add(SOURCE.text[:i].rstrip()[-1])
    SOURCE.move_index( "\\]" )

def _round_equation(SOURCE, CLEAN, folder_path):
    """ add [_] when meeting an equation called via \( and move index to the end if it """
    i = SOURCE.text.find( "\\)" )
    CLEAN.add("[_]")
    if SOURCE.text[:i].rstrip()[-1] in [",", ";", "."]: # add punctuation to non-inline equations
        CLEAN.add(SOURCE.text[:i].rstrip()[-1])
    SOURCE.move_index( "\\)" )

def _apostrofe(SOURCE, CLEAN, folder_path):
    """ skip letter when meeting an apostrofe """
    if SOURCE.text[1] in ("a","e","i","o","u"):
        SOURCE.index += 1

def _tilde(SOURCE, CLEAN, folder_path):
    """ add tilde to CLEAN """
    CLEAN.add("~")
    SOURCE.index += 1

def _null_function(SOURCE, CLEAN, folder_path):
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

def interpret(SOURCE, CLEAN, command, folder_path):
    """ this is the custom interpreter that recalls first custom subroutines, then built-in subroutines and then skip the command if not recognised """
    if command:
        if command in void or command in void_c:
            pass
        elif command in dic_commands_c:
            dic_commands_c[command](SOURCE, CLEAN, command, folder_path)
        elif command in dic_commands:
            dic_commands[command](SOURCE, CLEAN, command, folder_path)
        else:
            while SOURCE.text[0] in ["{","["]: # check if opening and closing brackets
                if SOURCE.text[0] == "{":
                    i = SOURCE.text.find("{",1)
                    j = SOURCE.text.find("}",1)
                    while 0 < i < j:
                        i = SOURCE.text.find("{",i+1)
                        j = SOURCE.text.find("}",j+1)
                    SOURCE.index += j+1
                else:
                    i = SOURCE.text.find("[",1)
                    j = SOURCE.text.find("]",1)
                    while 0 < i < j:
                        i = SOURCE.text.find("[",i+1)
                        j = SOURCE.text.find("]",j+1)
                    SOURCE.index += j+1
            CLEAN.aggro.add(command)
    else: # empty string
        command = SOURCE.text[0]
        if command in special_commands:
            special_commands[command](SOURCE, CLEAN, folder_path)
        else:
            CLEAN.add(" ")
            SOURCE.index += 1


#----------------------------------------
