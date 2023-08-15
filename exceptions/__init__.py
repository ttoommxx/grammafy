#----------------------------------------
# BUILT-IN FUNCTIONS
#----------------------------------------

import os

def reprint(source, clean, command, folder_path):
    clean.add(command)

def curly(source, clean, command, folder_path):
    source.move_index("}")

def curly_curly(source, clean, command, folder_path):
    source.move_index("}")
    source.move_index("}")

def color(source, clean, command, folder_path):
    clean.add("Color:")
    i = source.text.find( "}" )
    clean.add(source.text[ 1:i ].upper())
    source.index += i+1

def footnote(source, clean, command, folder_path):
    i = 1
    j = i # index for open brackets
    while i >= j and j > 0 :
        i = source.text.find( "}",i ) +1
        j = source.text.find( "{",j ) +1

    # add the text in the footnote to the queue in parenthesis
    source.add("(FOOTNOTE: " + source.text[ 1:i-1 ] + ")")
    source.root.index += i

def include(source, clean, command, folder_path): # included files need to be in the same folder
    i = source.text.find("}")
    include_path = source.text[ 1:i ]
    if not include_path.endswith(".tex"): # if the extension is not present
        include_path += ".tex"
    with open(f"{folder_path}{include_path}") as include_tex:
        source.add( include_tex.read() )
    source.root.index += i+1

def print_curly(source, clean, command, folder_path):
    clean.add("[_]")
    source.move_index("}")

def print_square_curly(source, clean, command, folder_path):
    clean.add("[_]")
    if source.text[0] == "[":
        source.move_index("]")
    source.move_index("}")

from exceptions import sub_begin

def begin(source, clean, command, folder_path):
    i = source.text.find("}") # right next after the brackets
    command = source.text[ 1:i ] # remove asterisk if any
    source.move_index("}")
    sub_begin.interpret(source, clean, command, folder_path)
        
from exceptions import sub_end
        
def end(source, clean, command, folder_path):
    i = source.text.find("}")
    command = source.text[ 1:i ]
    source.move_index("}")
    sub_end.interpret(source, clean, command, folder_path)

# special commands (not include command to avoid string problems)

def new_line(source, clean, folder_path):
    clean.add("\n")
    source.index += 1

def square_equation(source, clean, folder_path):
    i = source.text.find( "\\]" )
    clean.add("[_]")
    if source.text[:i].rstrip()[-1] in [",", ";", "."]: # add punctuation to non-inline equations
        clean.add(source.text[:i].rstrip()[-1])
    source.move_index( "\\]" )

def round_equation(source, clean, folder_path):
    i = source.text.find( "\\)" )
    clean.add("[_]")
    if source.text[:i].rstrip()[-1] in [",", ";", "."]: # add punctuation to non-inline equations
        clean.add(source.text[:i].rstrip()[-1])
    source.move_index( "\\)" )

def apostrofe(source, clean, folder_path):
    if source.text[1] in ["a","e","i","o","u"]:
        source.index += 1

def tilde(source, clean, folder_path):
    clean.add("~")
    source.index += 1

def null_function(source, clean, folder_path):
    pass

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
    "addchap":curly,
    "addsec":curly,
    "begin":begin,
    "bibliography":curly,
    "bibliographystyle":curly,
    "chaptermark":curly,
    "cite":print_square_curly,
    "color":color,
    "cref":print_curly,
    "Cref":print_curly,
    "email":curly,
    "end":end,
    "eqref":print_curly,
    "fontfamily":curly,
    "footnote":footnote,
    "hspace":curly,
    "include":include,
    "includegraphics":curly,
    "input":include,
    "label":curly,
    "pagenumbering":curly,
    "pagestyle":curly,
    "ref":print_curly,
    "renewcommand":curly_curly,
    "setlength":curly_curly,
    "thispagestyle":curly,
    "vspace":curly,
    "&":reprint,
    "%":reprint,
    "#":reprint
}

special_commands = {
    "[":square_equation,
    "(":round_equation,
    "\"":apostrofe,
    "'":apostrofe,
    "\\":new_line,
    "\n":new_line,
    "~":tilde,
}

#----------------------------------------
# INTERPRETER
#----------------------------------------

def interpret(source, clean, command, folder_path):
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