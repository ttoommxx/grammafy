#----------------------------------------
# BULTI-IN FUNCTIONS
#----------------------------------------

def _title(SOURCE, CLEAN, command, folder_path):
    """ add title to CLEAN """
    CLEAN.add(command.title() + ".")

def _equation(SOURCE, CLEAN, command, folder_path):
    """ add [_] and move to the end of the equation command """
    CLEAN.add("[_]")
    # find the index where the whole portion ends
    i = SOURCE.text.find("\\end{" + command + "}") # from here, use regex
    if SOURCE.text[:i-1].rstrip()[-1] in [",", ";", "."]:
        CLEAN.add(SOURCE.text[:i-1].rstrip()[-1])
    SOURCE.move_index("\\end{" + command + "}")

def _enumerate(SOURCE, CLEAN, command, folder_path):
    """ add a new node to SOURCE, replacing item with . followed by a new number """
    if SOURCE.text[0] == "[":
        SOURCE.move_index("]")
    i = SOURCE.text.find("\\end{enumerate}")
    new_text = SOURCE.text[:i]
    index_enum = 1
    while "\\item" in new_text:
        new_text = new_text.replace("\\item", str(index_enum) + ".", 1)
        index_enum += 1

    SOURCE.add(new_text)
    SOURCE.root.move_index("\\end{enumerate}")

def _itemize(SOURCE, CLEAN, command, folder_path):
    """ add a new node to SOURCE, replacing item with - """
    if SOURCE.text[0] == "[":
        SOURCE.move_index("]")
    i = SOURCE.text.find("\\end{itemize}")
    new_text = SOURCE.text[:i].replace("\\item","-")

    SOURCE.add(new_text)
    SOURCE.root.move_index("\\end{itemize}")
    

def _curly_curly(SOURCE, CLEAN, command, folder_path):
    """ move index by two curly brackets """
    SOURCE.move_index("}")
    SOURCE.move_index("}")

def _curly_curly_curly(SOURCE, CLEAN, command, folder_path):
    """ move index by 3 curly brackets """
    for _ in range(3):
        SOURCE.move_index("}")

def _skip(SOURCE, CLEAN, command, folder_path):
    """ skip command when not recognised """
    SOURCE.move_index("\\end{" + command + "}")

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

def interpret(SOURCE, CLEAN, command, folder_path):
    """ custom interpreted for the begin routine, works similarly to the main interpreter """ 
    if command in void or command in void_c:
        pass
    elif command in dic_commands_c:
        dic_commands_c[command](SOURCE, CLEAN, command, folder_path)
    elif command in dic_commands:
        dic_commands[command](SOURCE, CLEAN, command, folder_path)
    else:
        i = SOURCE.text.find("\\begin{" + command + "}", 6)
        j = SOURCE.text.find("\\end{" + command + "}",6)
        while 0 < i < j: # in case the class is nested
            i = SOURCE.text.find("\\begin{" + command + "}", i+6)
            j = SOURCE.text.find("\\end{" + command + "}", j+6)
        SOURCE.index += j + 5 + len(command)
        CLEAN.aggro.add("begin{" + command + "}")