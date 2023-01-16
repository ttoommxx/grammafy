writeBegin = writeBegin + '[1]'

# find the index where the whole portion ends
i = readBegin.find('\\end{tikzpicture}')
if readBegin[:i-1].replace(' ','').replace('\n','').replace('$','')[-1] in [',', ';', '.']:
                writeBegin = writeBegin + readBegin[:i-1].replace(' ','').replace('\n','').replace('$','')[-1]

i = i + 17 # skipping to the end of the program 
readBegin = readBegin[i:]
