clean += "[_]"
if source.tex[0] == "[":
    source.move_index("]")
source.move_index("}")