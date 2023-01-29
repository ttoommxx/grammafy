CLEAN = CLEAN + '[_]'

# find the index where the whole portion ends
i = SOURCE.find('\\end{table}') + 11
 
SOURCE = SOURCE[i:]
