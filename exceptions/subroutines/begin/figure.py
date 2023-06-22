CLEAN += "[_]"

# find the index where the whole portion ends
i = SOURCE[-2].find("\\end{figure}",SOURCE[-1]) + 12
SOURCE[-1] = i
