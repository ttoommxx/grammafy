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
    "corollary":"corollary",
    "definition":"definition",
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
    "wrapfigure":"curly_curly_curly"
}

from exceptions.sub_begin import routines_custom

#----------------------------------------
# BULTI-IN FUNCTIONS
#----------------------------------------

def title(source, clean, command):
    clean.tex += command.title() + "."

def equation(source, clean, command):
    clean.tex += "[_]"
    # find the index where the whole portion ends
    i = source.tex.find("\\end{" + command + "}") # from here, use regex
    if source.tex[:i-1].replace(" ","").replace("\n","").replace("$","")[-1] in [",", ";", "."]:
                    clean.tex += source.tex[:i-1].replace(" ","").replace("\n","").replace("$","")[-1]
    source.move_index("\\end{" + command + "}")

def enumerate(source, clean, command):
    if source.tex[0] == "[":
        source.move_index("]")
    i = source.tex.find("\\end{enumerate}")
    new_text = source.tex[:i]

    index_enum = 1
    while "\\item" in new_text:
        new_text = new_text.replace("\\item", str(index_enum) + ".", 1)
        index_enum += 1

    source.add(new_text)
    source.root.move_index("\\end{enumerate}")

def curly_curly(source, clean, command):
    source.move_index("}")
    source.move_index("}")

def curly_curly_curly(source, clean, command):
    for _ in range(3):
        source.move_index("}")

def skip(source, clean, command):
    source.move_index("\\end{" + command + "}")

#----------------------------------------
# INTERPRETER
#----------------------------------------

def interpret(source, clean, command):
    if command in void or command in void_c:
        pass
    elif command in dic_commands_c:
        exec(dic_commands_c[command] + f"(source, clean, {command})")
    elif command in dic_commands:
        exec(dic_commands[command] + f"(source, clean, {command})")
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
        clean.aggro.add("begin{" + command + "}")