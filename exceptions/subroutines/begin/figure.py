clean += "[_]"

# find the index where the whole portion ends

i = min(( source.tex.find(x) for x in ["\\end{figure*}", "\\end{figure}"] if x in source.tex ))
i = i + 12 + (source.tex[12] == "*") # skipping to the end of the program 
source.index += i
