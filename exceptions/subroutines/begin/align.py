writeBegin = writeBegin + '[1]'

# find the index where the whole portion ends
i = min([readBegin.find(x) for x in ['\\end{align*}', '\\end{align}'] if readBegin.find(x)>-1])
if readBegin[:i-1].replace(' ','').replace('\n','').replace('$','')[-1] in [',', ';', '.']:
                writeBegin = writeBegin + readBegin[:i-1].replace(' ','').replace('\n','').replace('$','')[-1]

i = i + 11 + (readBegin[11] == '*') # skipping to the end of the program 
readBegin = readBegin[i:]
