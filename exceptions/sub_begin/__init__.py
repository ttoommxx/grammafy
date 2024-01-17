#----------------------------------------
# BULTI-IN FUNCTIONS
#----------------------------------------

def _title(source, clean, command, folder_path):
    """ add title to clean """
    clean.add(command.title() + ".")

def _equation(source, clean, command, folder_path):
    """ add [_] and move to the end of the equation command """
    clean.add("[_]")
    # find the index where the whole portion ends
    i = source.text.find("\\end{" + command + "}") # from here, use regex
    if source.text[:i-1].rstrip()[-1] in [",", ";", "."]:
        clean.add(source.text[:i-1].rstrip()[-1])
    source.move_index("\\end{" + command + "}")

def _enumerate(source, clean, command, folder_path):
    """ add a new node to source, replacing item with . followed by a new number """
    if source.text[0] == "[":
        source.move_index("]")
    i = source.text.find("\\end{enumerate}")
    new_text = source.text[:i]
    index_enum = 1
    while "\\item" in new_text:
        new_text = new_text.replace("\\item", str(index_enum) + ".", 1)
        index_enum += 1

    source.add(new_text)
    source.root.move_index("\\end{enumerate}")

def _itemize(source, clean, command, folder_path):
    """ add a new node to source, replacing item with - """
    if source.text[0] == "[":
        source.move_index("]")
    i = source.text.find("\\end{itemize}")
    new_text = source.text[:i].replace("\\item","-")

    source.add(new_text)
    source.root.move_index("\\end{itemize}")
    

def _curly_curly(source, clean, command, folder_path):
    """ move index by two curly brackets """
    source.move_index("}")
    source.move_index("}")

def _curly_curly_curly(source, clean, command, folder_path):
    """ move index by 3 curly brackets """
    for _ in range(3):
        source.move_index("}")

def _skip(source, clean, command, folder_path):
    """ skip command when not recognised """
    source.move_index("\\end{" + command + "}")

#----------------------------------------
# VARIABLES
#----------------------------------------

from exceptions.sub_begin.begin_custom import void_c

void = (
    "center",
    "frame"
)

from exceptions.sub_begin.begin_custom import dic_commands_c

dic_commands = {
    "abstract":_title,
    "align":_equation,
    "align*":_equation,
    "equation":_equation,
    "equation*":_equation,
    "comment":_title,
    "conjecture":_title,
    "corollary":_title,
    "definition":_title,
    "enumerate":_enumerate,
    "eqnarray":_equation,
    "eqnarray*":_equation,
    "figure":_equation,
    "figure*":_equation,
    "gather":_equation,
    "gather*":_equation,
    "lemma":_title,
    "minipage":_curly_curly,
    "multline":_equation,
    "multline*":_equation,
    "proof":_title,
    "proposition":_title,
    "question":_title,
    "remark":_title,
    "table":_equation,
    "thebibliography":_skip,
    "theorem":_title,
    "tikzpicture":_equation,
    "verbatim":_equation,
    "wrapfigure":_curly_curly_curly,
    "itemize":_itemize,
}

#----------------------------------------
# INTERPRETER
#----------------------------------------

def interpret(source, clean, command, folder_path):
    """ custom interpreted for the begin routine, works similarly to the main interpreter """ 
    if command in void or command in void_c:
        pass
    elif command in dic_commands_c:
        dic_commands_c[command](source, clean, command, folder_path)
    elif command in dic_commands:
        dic_commands[command](source, clean, command, folder_path)
    else:
        i = source.text.find("\\begin{" + command + "}", 6)
        j = source.text.find("\\end{" + command + "}",6)
        while 0 < i < j: # in case the class is nested
            i = source.text.find("\\begin{" + command + "}", i+6)
            j = source.text.find("\\end{" + command + "}", j+6)
        source.index += j + 5 + len(command)
        clean.aggro.add("begin{" + command + "}")