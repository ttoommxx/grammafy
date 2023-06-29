from exceptions.void_custom import void_c

void = [
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
]

from exceptions.dictionary_commands_custom import dic_commands_c

dic_commands = {
    "addchap":"routines.curly",
    "addsec":"routines.curly",
    "begin":"routines.begin",
    "bibliography":"routines.curly",
    "bibliographystyle":"routines.curly",
    "chaptermark":"routines.curly",
    "cite":"routines.print_square_curly",
    "color":"routines.color",
    "cref":"routines.print_curly",
    "Cref":"routines.print_curly",
    "email":"routines.curly",
    "end":"routines.end",
    "eqref":"routines.print_curly",
    "fontfamily":"routines.curly",
    "footnote":"routines.footnote",
    "hspace":"routines.curly",
    "include":"routines.include",
    "includegraphics":"routines.curly",
    "input":"routines.include",
    "item":"routines.dash",
    "label":"routines.curly",
    "pagenumbering":"routines.curly",
    "pagestyle":"routines.curly",
    "ref":"routines.print_curly",
    "renewcommand":"routines.curly_curly",
    "setlength":"routines.curly_curly",
    "thispagestyle":"routines.curly",
    "vspace":"routines.curly"
}

from exceptions import routines, routines_custom

def interpret(source, clean, command):
    if command in void or command in void_c:
        pass
    elif command in dic_commands_c:
        exec(dic_commands_c[command] + f"(source, clean, {command})")
    elif command in dic_commands:
        exec( dic_commands[command] + f"(source, clean, {command})")
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