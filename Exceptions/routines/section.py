#remove curly brackets starting at 1 instead of 0
t = 1
while readText[t] != '}':
    writeText = writeText + readText[t]
    t=t+1
j = j+t
