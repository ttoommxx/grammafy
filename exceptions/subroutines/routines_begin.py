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