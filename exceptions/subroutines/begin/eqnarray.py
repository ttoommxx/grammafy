CLEAN = CLEAN + '[1]'

# find the index where the whole portion ends
i = min([SOURCE.find(x) for x in ['\\end{eqnarray*}', '\\end{eqnarray}'] if SOURCE.find(x)>-1])
if SOURCE[:i-1].replace(' ','').replace('\n','').replace('$','')[-1] in [',', ';', '.']:
                CLEAN = CLEAN + SOURCE[:i-1].replace(' ','').replace('\n','').replace('$','')[-1]

i = i + 14 + (SOURCE[14] == '*') # skipping to the end of the program 
SOURCE = SOURCE[i:]