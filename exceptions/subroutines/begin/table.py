CLEAN += "[_]"

# find the index where the whole portion ends
i = SOURCE[-2].find("\\end{table}",next_elem) + 11
 
SOURCE[-1] = i
