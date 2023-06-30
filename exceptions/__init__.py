#----------------------------------------
# VARIABLES
#----------------------------------------

from exceptions.void_custom import void_c

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

from exceptions.dictionary_commands_custom import dic_commands_c

dic_commands = {
    "addchap":"curly",
    "addsec":"curly",
    "begin":"begin",
    "bibliography":"curly",
    "bibliographystyle":"curly",
    "chaptermark":"curly",
    "cite":"print_square_curly",
    "color":"color",
    "cref":"print_curly",
    "Cref":"print_curly",
    "email":"curly",
    "end":"end",
    "eqref":"print_curly",
    "fontfamily":"curly",
    "footnote":"footnote",
    "hspace":"curly",
    "include":"include",
    "includegraphics":"curly",
    "input":"include",
    "item":"dash",
    "label":"curly",
    "pagenumbering":"curly",
    "pagestyle":"curly",
    "ref":"print_curly",
    "renewcommand":"curly_curly",
    "setlength":"curly_curly",
    "thispagestyle":"curly",
    "vspace":"curly"
}

from exceptions import routines_custom

#----------------------------------------
# BUILT-IN FUNCTIONS
#----------------------------------------

import os

def curly(source, clean, command, folder_path):
    source.move_index("}")

def curly_curly(source, clean, command, folder_path):
    source.move_index("}")
    source.move_index("}")

def color(source, clean, command, folder_path):
    clean.tex += "Color:"
    i = source.tex.find( "}" )
    clean.tex += source.tex[ 1:i ].upper()
    source.index += i+1

def dash(source, clean, command, folder_path):
    clean.tex += "-"

def footnote(source, clean, command, folder_path):
    i = 1
    j = i # index for open brackets
    while i >= j and j > 0 :
        i = source.tex.find( "}",i ) +1
        j = source.tex.find( "{",j ) +1

    # add the text in the footnote to the queue in parenthesis
    source.add("(FOOTNOTE: " + source.tex[ 1:i-1 ] + ")")
    source.root.index += i

def include(source, clean, command, folder_path): # included files need to be in the same folder
    i = source.tex.find("}")
    include_path = source.tex[ 1:i ]
    if not include_path.endswith(".tex"): # if the extension is not present
        include_path += ".tex"
    with open(f"{folder_path}{include_path}") as include_tex:
        source.add( include_tex.read() )
    source.root.index += i+1

def print_curly(source, clean, command, folder_path):
    clean.tex += "[_]"
    source.move_index("}")

def print_square_curly(source, clean, command, folder_path):
    clean.tex += "[_]"
    if source.tex[0] == "[":
        source.move_index("]")
    source.move_index("}")

from exceptions import sub_begin

def begin(source, clean, command, folder_path):
    i = source.tex.find("}") # right next after the brackets
    command = source.tex[ 1:i ] # remove asterisk if any
    source.move_index("}")
    sub_begin.interpret(source, clean, command, folder_path)
        
from exceptions import sub_end
        
def end(source, clean, command, folder_path):
    i = source.tex.find("}")
    command = source.tex[ 1:i ]
    source.move_index("}")
    sub_end.interpret(source, clean, command, folder_path)

#----------------------------------------
# INTERPRETER
#----------------------------------------

def interpret(source, clean, command, folder_path):
    if command in void or command in void_c:
        pass
    elif command in dic_commands_c:
        exec(dic_commands_c[command] + "(source, clean,\"" + command + "\", folder_path)")
    elif command in dic_commands:
        exec(dic_commands[command] + "(source, clean,\"" + command + "\", folder_path)")
    else:
        while source.tex[0] in ["{","["]: # check if opening and closing brackets
            if source.tex[0] == "{":
                i = source.tex.find("{",1)
                j = source.tex.find("}",1)
                while 0 < i < j:
                    i = source.tex.find("{",i+1)
                    j = source.tex.find("}",j+1)
                source.index += j+1
            else:
                i = source.tex.find("[",1)
                j = source.tex.find("]",1)
                while 0 < i < j:
                    i = source.tex.find("[",i+1)
                    j = source.tex.find("]",j+1)
                source.index += j+1
        clean.aggro.add(command)

#----------------------------------------