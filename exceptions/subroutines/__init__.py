void_begin = [
    "center",
]

from exceptions.subroutines.void_begin_custom import void_begin_c

dic_commands_sub = {
    "abstract":"routines_begin.title",
    "align":"routines_begin.equation",
    "align*":"routines_begin.equation",
    "equation":"routines_begin.equation",
    "equation*":"routines_begin.equation",
    "comment":"routines_begin.title",
    "conjecture":"routines_begin.title",
    "corollary":"routines_begin.corollary",
    "definition":"routines_begin.definition",
    "enumerate":"routines_begin.enumerate",
    "eqnarray":"routines_begin.equation",
    "eqnarray*":"routines_begin.equation",
    "figure":"routines_begin.equation",
    "figure*":"routines_begin.equation",
    "gather":"routines_begin.equation",
    "gather*":"routines_begin.equation",
    "lemma":"routines_begin.title",
    "minipage":"routines_begin.curly_curly",
    "multline":"routines_begin.equation",
    "multline*":"routines_begin.equation",
    "proof":"routines_begin.title",
    "proposition":"routines_begin.title",
    "question":"routines_begin.title",
    "remark":"routines_begin.title",
    "table":"routines_begin.equation",
    "thebibliography":"routines_begin.skip",
    "theorem":"routines_begin.title",
    "tikzpicture":"routines_begin.equation",
    "verbatim":"routines_begin.equation",
    "wrapfigure":"routines_begin.curly_curly_curly"
}

from exceptions.subroutines import routines_begin, routines_begin_custom

def interpret_begin(source, clean, command):
    if command in void_begin or command in void_begin_c:
        pass
    elif command in dic_commands_sub_c: # from here create dic command sub c
        exec(dic_commands_c_sub[command] + f"(source, clean, {command})")
    elif command in dic_commands_sub:
        exec( dic_commands_sub[command] + f"(source, clean, {command})")
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
        clean.aggro.add(f"begin - {command}")

# from here things for end routine