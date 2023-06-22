CLEAN += "[_]"

# find the index where the whole portion ends
i = SOURCE[-2].find("\\end{figure}",next_elem) + 12
SOURCE[-1] = i
