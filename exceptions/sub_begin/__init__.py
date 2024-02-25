"""being routines initialiser"""

# ----------------------------------------
# BULTI-IN FUNCTIONS
# ----------------------------------------


def _title(ENV) -> None:
    """add title to ENV.clean"""
    ENV.clean.add(ENV.command.title() + ".")


def _equation(ENV) -> None:
    """add [_] and move to the end of the equation command"""
    ENV.clean.add("[_]")
    # find the index where the whole portion ends
    i = ENV.source.text.find("\\end{" + ENV.command + "}")  # from here, use regex
    if ENV.source.text[: i - 1].rstrip()[-1] in [",", ";", "."]:
        ENV.clean.add(ENV.source.text[: i - 1].rstrip()[-1])
    ENV.source.move_index("\\end{" + ENV.command + "}")


def _enumerate(ENV) -> None:
    """add a new node to ENV.source, replacing item with . followed by a new number"""
    if ENV.source.text[0] == "[":
        ENV.source.move_index("]")
    i = ENV.source.text.find("\\end{enumerate}")
    new_text = ENV.source.text[:i]
    index_enum = 1
    while "\\item" in new_text:
        new_text = new_text.replace("\\item", str(index_enum) + ".", 1)
        index_enum += 1

    ENV.source.add(new_text)
    ENV.source.root.move_index("\\end{enumerate}")


def _itemize(ENV) -> None:
    """add a new node to ENV.source, replacing item with -"""
    if ENV.source.text[0] == "[":
        ENV.source.move_index("]")
    i = ENV.source.text.find("\\end{itemize}")
    new_text = ENV.source.text[:i].replace("\\item", "-")

    ENV.source.add(new_text)
    ENV.source.root.move_index("\\end{itemize}")


def _curly_curly(ENV) -> None:
    """move index by two curly brackets"""
    ENV.source.move_index("}")
    ENV.source.move_index("}")


def _curly_curly_curly(ENV) -> None:
    """move index by 3 curly brackets"""
    for _ in range(3):
        ENV.source.move_index("}")


def _skip(ENV) -> None:
    """skip command when not recognised"""
    ENV.source.move_index("\\end{" + ENV.command + "}")


# ----------------------------------------
# VARIABLES
# ----------------------------------------

from exceptions.sub_begin.begin_custom import void_c

void = ("center", "frame")

from exceptions.sub_begin.begin_custom import dic_commands_c

dic_commands = {
    "abstract": _title,
    "align": _equation,
    "align*": _equation,
    "equation": _equation,
    "equation*": _equation,
    "comment": _title,
    "conjecture": _title,
    "corollary": _title,
    "definition": _title,
    "enumerate": _enumerate,
    "eqnarray": _equation,
    "eqnarray*": _equation,
    "figure": _equation,
    "figure*": _equation,
    "gather": _equation,
    "gather*": _equation,
    "lemma": _title,
    "minipage": _curly_curly,
    "multline": _equation,
    "multline*": _equation,
    "proof": _title,
    "proposition": _title,
    "question": _title,
    "remark": _title,
    "table": _equation,
    "thebibliography": _skip,
    "theorem": _title,
    "tikzpicture": _equation,
    "verbatim": _equation,
    "wrapfigure": _curly_curly_curly,
    "itemize": _itemize,
}

# ----------------------------------------
# INTERPRETER
# ----------------------------------------


def interpret(ENV) -> None:
    """custom interpreted for the begin routine, works similarly to the main interpreter"""
    if ENV.command in void or ENV.command in void_c:
        pass
    elif ENV.command in dic_commands_c:
        dic_commands_c[ENV.command](ENV)
    elif ENV.command in dic_commands:
        dic_commands[ENV.command](ENV)
    else:
        i = ENV.source.text.find("\\begin{" + ENV.command + "}", 6)
        j = ENV.source.text.find("\\end{" + ENV.command + "}", 6)
        while 0 < i < j:  # in case the class is nested
            i = ENV.source.text.find("\\begin{" + ENV.command + "}", i + 6)
            j = ENV.source.text.find("\\end{" + ENV.command + "}", j + 6)
        ENV.source.index += j + 5 + len(ENV.command)
        ENV.clean.aggro.add("begin{" + ENV.command + "}")
