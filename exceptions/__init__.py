"""routine modules initialiser"""
from typing import NoReturn, TypeVar

EnvVar = TypeVar("EnvVar")

# ----------------------------------------
# BUILT-IN FUNCTIONS
# ----------------------------------------


def _reprint(ENV: EnvVar) -> NoReturn:
    """add the command to ENV.clean the command"""
    ENV.clean.add(ENV.command)


def _curly(ENV: EnvVar) -> NoReturn:
    """move to the end of curly brackets"""
    ENV.source.move_index("}")


def _curly_curly(ENV: EnvVar) -> NoReturn:
    """move to the end for 2 consecutive curly brackets"""
    ENV.source.move_index("}")
    ENV.source.move_index("}")


def _color(ENV: EnvVar) -> NoReturn:
    """add color to ENV.source and move to the end of curly brackets"""
    ENV.clean.add("Color:")
    i = ENV.source.text.find("}")
    ENV.clean.add(ENV.source.text[1:i].upper())
    ENV.source.index += i + 1


def _footnote(ENV: EnvVar) -> NoReturn:
    """add footnote to ENV.source and move to the end of nested curly brackets"""
    i = 1
    j = i  # index for open brackets
    while i >= j and j > 0:
        i = ENV.source.text.find("}", i) + 1
        j = ENV.source.text.find("{", j) + 1

    # add the text in the footnote to the queue in parenthesis
    ENV.source.add("(FOOTNOTE: " + ENV.source.text[1 : i - 1] + ")")
    ENV.source.root.index += i


def _include(ENV: EnvVar) -> NoReturn:
    r"""responds to \include command and adds the new ENV.source to the head of ENV.source. The included files need to be in the same folder"""
    i = ENV.source.text.find("}")
    include_path = ENV.source.text[1:i]
    if not include_path.endswith(".tex"):  # if the extension is not present
        include_path += ".tex"
    with open(f"{folder_path}{include_path}", encoding="utf-8") as include_tex:
        ENV.source.add(include_tex.read())
    ENV.source.root.index += i + 1


def _print_curly(ENV: EnvVar) -> NoReturn:
    """[_] to ENV.clean when meeting curly brackets and move to the end of curly brackets"""
    ENV.clean.add("[_]")
    ENV.source.move_index("}")


def _print_square_curly(ENV: EnvVar) -> NoReturn:
    """add [_] for ENV.clean and move to the end of square if present, and then curly brackets"""
    ENV.clean.add("[_]")
    if ENV.source.text[0] == "[":
        ENV.source.move_index("]")
    ENV.source.move_index("}")


from exceptions import sub_begin


def _begin(ENV: EnvVar) -> NoReturn:
    """responds to the command being and move to the function begin and its subroutines"""
    i = ENV.source.text.find("}")  # right next after the brackets
    ENV.command = ENV.source.text[1:i]  # remove asterisk if any
    ENV.source.move_index("}")
    sub_begin.interpret(ENV)


from exceptions import sub_end


def _end(ENV: EnvVar) -> NoReturn:
    """responds to the command end and move to the function end and its subroutines"""
    i = ENV.source.text.find("}")
    ENV.command = ENV.source.text[1:i]
    ENV.source.move_index("}")
    sub_end.interpret(ENV)


# special commands (not include command to avoid string problems)


def _new_line(ENV: EnvVar) -> NoReturn:
    """add a new line to ENV.clean"""
    ENV.clean.add("\n")
    ENV.source.index += 1


def _square_equation(ENV: EnvVar) -> NoReturn:
    r"""add [_] when meeting an equation called via \[ and move index to the end if it"""
    i = ENV.source.text.find("\\]")
    ENV.clean.add("[_]")
    if ENV.source.text[:i].rstrip()[-1] in [
        ",",
        ";",
        ".",
    ]:  # add punctuation to non-inline equations
        ENV.clean.add(ENV.source.text[:i].rstrip()[-1])
    ENV.source.move_index("\\]")


def _round_equation(ENV: EnvVar) -> NoReturn:
    r"""add [_] when meeting an equation called via \( and move index to the end if it"""
    i = ENV.source.text.find("\\)")
    ENV.clean.add("[_]")
    if ENV.source.text[:i].rstrip()[-1] in [
        ",",
        ";",
        ".",
    ]:  # add punctuation to non-inline equations
        ENV.clean.add(ENV.source.text[:i].rstrip()[-1])
    ENV.source.move_index("\\)")


def _apostrofe(ENV: EnvVar) -> NoReturn:
    """skip letter when meeting an apostrofe"""
    if ENV.source.text[1] in ("a", "e", "i", "o", "u"):
        ENV.source.index += 1


def _tilde(ENV: EnvVar) -> NoReturn:
    """add tilde to ENV.clean"""
    ENV.clean.add("~")
    ENV.source.index += 1


def _null_function(ENV: EnvVar) -> NoReturn:
    """null function, does nothing"""


# ----------------------------------------
# VARIABLES
# ----------------------------------------

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
    "texttt",
)

from exceptions.routines_custom import dic_commands_c

dic_commands = {
    "addchap": _curly,
    "addsec": _curly,
    "begin": _begin,
    "bibliography": _curly,
    "bibliographystyle": _curly,
    "chaptermark": _curly,
    "cite": _print_square_curly,
    "color": _color,
    "cref": _print_curly,
    "Cref": _print_curly,
    "email": _curly,
    "end": _end,
    "eqref": _print_curly,
    "fontfamily": _curly,
    "footnote": _footnote,
    "hspace": _curly,
    "include": _include,
    "includegraphics": _curly,
    "input": _include,
    "label": _curly,
    "pagenumbering": _curly,
    "pagestyle": _curly,
    "ref": _print_curly,
    "renewcommand": _curly_curly,
    "setlength": _curly_curly,
    "thispagestyle": _curly,
    "vspace": _curly,
    "&": _reprint,
    "%": _reprint,
    "#": _reprint,
}

special_commands = {
    "[": _square_equation,
    "(": _round_equation,
    '"': _apostrofe,
    "'": _apostrofe,
    "\\": _new_line,
    "\n": _new_line,
    "~": _tilde,
}

# ----------------------------------------
# INTERPRETER
# ----------------------------------------


def interpret(ENV: EnvVar) -> NoReturn:
    """this is the custom interpreter that recalls first custom subroutines, then built-in subroutines and then skip the command if not recognised"""
    if ENV.command:
        if ENV.command in void or ENV.command in void_c:
            pass
        elif ENV.command in dic_commands_c:
            dic_commands_c[ENV.command](ENV)
        elif ENV.command in dic_commands:
            dic_commands[ENV.command](ENV)
        else:
            while ENV.source.text[0] in [
                "{",
                "[",
            ]:  # check if opening and closing brackets
                if ENV.source.text[0] == "{":
                    i = ENV.source.text.find("{", 1)
                    j = ENV.source.text.find("}", 1)
                    while 0 < i < j:
                        i = ENV.source.text.find("{", i + 1)
                        j = ENV.source.text.find("}", j + 1)
                    ENV.source.index += j + 1
                else:
                    i = ENV.source.text.find("[", 1)
                    j = ENV.source.text.find("]", 1)
                    while 0 < i < j:
                        i = ENV.source.text.find("[", i + 1)
                        j = ENV.source.text.find("]", j + 1)
                    ENV.source.index += j + 1
            ENV.clean.aggro.add(ENV.command)
    else:  # empty string
        ENV.command = ENV.source.text[0]
        if ENV.command in special_commands:
            special_commands[ENV.command](ENV)
        else:
            ENV.clean.add(" ")
            ENV.source.index += 1


# ----------------------------------------
