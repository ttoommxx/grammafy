#----------------------------------------
# VARIABLES
#----------------------------------------

from exceptions.sub_begin.void_custom import void_c

void = (
    "center",
)

from exceptions.sub_begin.dictionary_commands_custom import dic_commands_c

dic_commands = {
    "abstract":"title",
    "align":"equation",
    "align*":"equation",
    "equation":"equation",
    "equation*":"equation",
    "comment":"title",
    "conjecture":"title",
    "corollary":"title",
    "definition":"title",
    "enumerate":"enumerate",
    "eqnarray":"equation",
    "eqnarray*":"equation",
    "figure":"equation",
    "figure*":"equation",
    "gather":"equation",
    "gather*":"equation",
    "lemma":"title",
    "minipage":"curly_curly",
    "multline":"equation",
    "multline*":"equation",
    "proof":"title",
    "proposition":"title",
    "question":"title",
    "remark":"title",
    "table":"equation",
    "thebibliography":"skip",
    "theorem":"title",
    "tikzpicture":"equation",
    "verbatim":"equation",
    "wrapfigure":"curly_curly_curly",
    "itemize":"itemize",
}

from exceptions.sub_begin import routines_custom

#----------------------------------------
# BULTI-IN FUNCTIONS
#----------------------------------------

def title(source, clean, command, folder_path):
    clean.text += command.title() + "."

def equation(source, clean, command, folder_path):
    clean.text += "[_]"
    # find the index where the whole portion ends
    i = source.text.find("\\end{" + command + "}") # from here, use regex
    if source.text[:i-1].rstrip()[-1] in [",", ";", "."]:
        clean.text += source.text[:i-1].rstrip()[-1]
    source.move_index("\\end{" + command + "}")

def enumerate(source, clean, command, folder_path):
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

def itemize(source, clean, command, folder_path):
    if source.text[0] == "[":
        source.move_index("]")
    i = source.text.find("\\end{itemize}")
    new_text = source.text[:i].replace("\\item","-")

    source.add(new_text)
    source.root.move_index("\\end{itemize}")
    

def curly_curly(source, clean, command, folder_path):
    source.move_index("}")
    source.move_index("}")

def curly_curly_curly(source, clean, command, folder_path):
    for _ in range(3):
        source.move_index("}")

def skip(source, clean, command, folder_path):
    source.move_index("\\end{" + command + "}")

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
        i = source.text.find("\\begin{" + command + "}", 6)
        j = source.text.find("\\end{" + command + "}",6)
        while 0 < i < j: # in case the class is nested
            i = source.text.find("\\begin{" + command + "}", i+6)
            j = source.text.find("\\end{" + command + "}", j+6)
        source.index += j + 5 + len(command)
        clean.aggro.add("begin{" + command + "}")