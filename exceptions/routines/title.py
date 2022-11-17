#remove curly brackets starting at 1 instead of 0
t = 1
while readText[t] != '}':
    writeText = writeText + readText[t].upper()
    t=t+1
writeText = writeText + '.\n'
j = j+t
