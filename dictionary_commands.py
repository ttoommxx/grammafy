from dictionary_commands_custom import *

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

def interpret(command):
    