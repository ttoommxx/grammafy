CLEAN = CLEAN + '[_]'

# find the index where the whole portion ends
i = SOURCE.find('\\end{figure}') + 12
SOURCE = SOURCE[i:]
