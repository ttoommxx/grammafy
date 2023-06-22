CLEAN += "[_]"

# find the index where the whole portion ends
i = SOURCE[-2].find("\\end{table}",SOURCE[-1]) + 11
 
SOURCE[-1] = i
