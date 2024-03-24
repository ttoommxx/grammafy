"""being routines initialiser"""

# ----------------------------------------
# BULTI-IN FUNCTIONS
# ----------------------------------------


def _title(env) -> None:
    """add title to env.clean"""
    env.clean.add(env.command.title() + ".")


def _equation(env) -> None:
    """add [_] and move to the end of the equation command"""
    env.clean.add("[_]")
    # find the index where the whole portion ends
    i = env.source.text.find("\\end{" + env.command + "}")  # from here, use regex
    if env.source.text[: i - 1].rstrip()[-1] in [",", ";", "."]:
        env.clean.add(env.source.text[: i - 1].rstrip()[-1])
    env.source.move_index("\\end{" + env.command + "}")


def _enumerate(env) -> None:
    """add a new node to env.source, replacing item with . followed by a new number"""
    if env.source.text[0] == "[":
        env.source.move_index("]")
    i = env.source.text.find("\\end{enumerate}")
    new_text = env.source.text[:i]
    index_enum = 1
    while "\\item" in new_text:
        new_text = new_text.replace("\\item", str(index_enum) + ".", 1)
        index_enum += 1

    env.source.add(new_text)
    env.source.root.move_index("\\end{enumerate}")


def _itemize(env) -> None:
    """add a new node to env.source, replacing item with -"""
    if env.source.text[0] == "[":
        env.source.move_index("]")
    i = env.source.text.find("\\end{itemize}")
    new_text = env.source.text[:i].replace("\\item", "-")

    env.source.add(new_text)
    env.source.root.move_index("\\end{itemize}")


def _curly_curly(env) -> None:
    """move index by two curly brackets"""
    env.source.move_index("}")
    env.source.move_index("}")


def _curly_curly_curly(env) -> None:
    """move index by 3 curly brackets"""
    for _ in range(3):
        env.source.move_index("}")


def _skip(env) -> None:
    """skip command when not recognised"""
    env.source.move_index("\\end{" + env.command + "}")


# ----------------------------------------
# VARIABLES
# ----------------------------------------

from .begin_custom import void_c

void = ("center", "frame")

from .begin_custom import dic_commands_c

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


def interpret(env) -> None:
    """custom interpreted for the begin routine, works similarly to the main interpreter"""
    if env.command in void or env.command in void_c:
        pass
    elif env.command in dic_commands_c:
        dic_commands_c[env.command](env)
    elif env.command in dic_commands:
        dic_commands[env.command](env)
    else:
        i = env.source.text.find("\\begin{" + env.command + "}", 6)
        j = env.source.text.find("\\end{" + env.command + "}", 6)
        while 0 < i < j:  # in case the class is nested
            i = env.source.text.find("\\begin{" + env.command + "}", i + 6)
            j = env.source.text.find("\\end{" + env.command + "}", j + 6)
        env.source.index += j + 5 + len(env.command)
        env.clean.aggro.add("begin{" + env.command + "}")
