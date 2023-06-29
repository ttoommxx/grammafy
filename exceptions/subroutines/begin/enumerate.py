if source.tex[0] == "[":
    source.move_index("]")
i = source.tex.find("\\end{enumerate}")
new_text = source.tex[:i]

index_enum = 1
while "\\item" in new_text:
    new_text = new_text.replace("\\item", str(index_enum) + ".", 1)
    index_enum += 1

source = source.add(new_text)
source.root.move_index("\\end{enumerate}")