CLEAN = CLEAN + '(' # first add a parenthesis

i = 1
j = i # index for open brackets
while i >= j and j>0 :
    i = SOURCE.find('}',i) +1
    j = SOURCE.find('{',j) +1

SOURCE = SOURCE[1:i-1] + ')' + SOURCE[i:] # I just add the end of parenthesis in the SOURCE so that the program runs properly within the footnote content