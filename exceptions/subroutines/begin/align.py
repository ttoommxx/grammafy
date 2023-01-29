CLEAN = CLEAN + '[_]'

# find the index where the whole portion ends
i = min([SOURCE.find(x) for x in ['\\end{align*}', '\\end{align}'] if SOURCE.find(x)>-1])
if SOURCE[:i-1].replace(' ','').replace('\n','').replace('$','')[-1] in [',', ';', '.']:
                CLEAN = CLEAN + SOURCE[:i-1].replace(' ','').replace('\n','').replace('$','')[-1]

i = i + 11 + (SOURCE[11] == '*') # skipping to the end of the program 
SOURCE = SOURCE[i:]
