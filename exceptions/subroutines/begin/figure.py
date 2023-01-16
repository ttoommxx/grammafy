writeBegin = writeBegin + '[1]'

# find the index where the whole portion ends
i = readBegin.find('\\end{figure}') + 12
readBegin = readBegin[i:]
