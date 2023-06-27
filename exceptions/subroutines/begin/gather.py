clean += "[_]"

# find the index where the whole portion ends
i = min(( source.tex.find(x) for x in ["\\end{gather*}", "\\end{gather}"] if x in source.tex ))
if source.tex[:i-1].replace(" ","").replace("\n","").replace("$","")[-1] in [",", ";", "."]:
                clean += source.tex[:i-1].replace(" ","").replace("\n","").replace("$","")[-1]

i = i + 12 + (source.tex[12] == "*") # skipping to the end of the program 
source.index += i